import { useState } from 'react'
import {
  AnalysisResponse,
  JumpType,
  BiologicalSex,
  TrainingLevel,
  PresignResponse,
} from '../types/api'
import { supabase } from '../lib/supabase'

const MAX_FILE_SIZE_BYTES = 200 * 1024 * 1024 // 200 MB

interface UseAnalysisState {
  file: File | null
  jumpType: JumpType
  loading: boolean
  uploadProgress: number
  metrics: AnalysisResponse | null
  error: string | null
  enableDebug: boolean
  sex: BiologicalSex | null
  age: number | null
  trainingLevel: TrainingLevel | null
}

interface UseAnalysisActions {
  setFile: (file: File | null) => void
  setJumpType: (jumpType: JumpType) => void
  setEnableDebug: (enable: boolean) => void
  setSex: (sex: BiologicalSex | null) => void
  setAge: (age: number | null) => void
  setTrainingLevel: (level: TrainingLevel | null) => void
  analyze: () => Promise<void>
  retry: () => Promise<void>
  reset: () => void
}

/**
 * Get the base API URL from environment or use relative proxy in development
 */
function getApiUrl(path: string): string {
  const baseApiUrl = import.meta.env.VITE_API_URL || ''
  return baseApiUrl ? `${baseApiUrl}${path}` : path
}

/**
 * Get the current Supabase auth token (if available)
 */
async function getAuthToken(): Promise<string | undefined> {
  if (!supabase) return undefined
  const {
    data: { session },
  } = await supabase.auth.getSession()
  return session?.access_token
}

const R2_UPLOAD_TIMEOUT_MS = 5 * 60 * 1000 // 5 minutes

/**
 * Upload a file directly to R2 via presigned PUT URL with progress tracking.
 * Returns a promise that resolves when the upload completes.
 */
function uploadToR2(
  uploadUrl: string,
  file: File,
  contentType: string,
  onProgress: (percent: number) => void,
): Promise<void> {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest()
    xhr.timeout = R2_UPLOAD_TIMEOUT_MS

    xhr.upload.addEventListener('progress', (event) => {
      if (event.lengthComputable) {
        const percent = (event.loaded / event.total) * 100
        onProgress(Math.round(percent))
      }
    })

    xhr.addEventListener('load', () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        resolve()
      } else {
        reject(new Error(`Upload to storage failed: ${xhr.status}`))
      }
    })

    xhr.addEventListener('error', () => {
      reject(new Error('Network error: Unable to upload video'))
    })

    xhr.addEventListener('abort', () => {
      reject(new Error('Upload was cancelled'))
    })

    xhr.addEventListener('timeout', () => {
      reject(new Error('Upload timed out. Please check your connection and try again.'))
    })

    xhr.open('PUT', uploadUrl)
    xhr.setRequestHeader('Content-Type', contentType)
    xhr.send(file)
  })
}

/**
 * Custom hook for managing video analysis state and logic.
 *
 * Uses a three-step presigned URL flow:
 * 1. POST /api/upload/presign → get presigned PUT URL + object key
 * 2. PUT to R2 directly (with progress tracking)
 * 3. POST /api/analyze with video_key (small JSON, no file)
 */
export function useAnalysis(): UseAnalysisState & UseAnalysisActions {
  const [file, setFile] = useState<File | null>(null)
  const [jumpType, setJumpType] = useState<JumpType>('cmj')
  const [loading, setLoading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [metrics, setMetrics] = useState<AnalysisResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [enableDebug, setEnableDebug] = useState(false)
  const [sex, setSex] = useState<BiologicalSex | null>(null)
  const [age, setAge] = useState<number | null>(null)
  const [trainingLevel, setTrainingLevel] = useState<TrainingLevel | null>(null)

  const analyze = async () => {
    if (!file) {
      setError('Please select a video file')
      return
    }

    if (file.size > MAX_FILE_SIZE_BYTES) {
      setError('Video file is too large. Maximum size is 200MB.')
      return
    }

    setLoading(true)
    setError(null)
    setMetrics(null)
    setUploadProgress(0)

    try {
      const token = await getAuthToken()
      const headers: Record<string, string> = {}
      if (token) {
        headers['Authorization'] = `Bearer ${token}`
      }

      // --- Step 1: Get presigned upload URL ---
      const presignForm = new FormData()
      presignForm.append('filename', file.name)
      presignForm.append('content_type', file.type || 'video/mp4')

      const presignRes = await fetch(getApiUrl('/api/upload/presign'), {
        method: 'POST',
        headers,
        body: presignForm,
      })

      if (!presignRes.ok) {
        const errBody = await presignRes.json().catch(() => null)
        throw new Error(
          errBody?.detail || errBody?.message || `Failed to get upload URL: ${presignRes.status}`,
        )
      }

      const presign: PresignResponse = await presignRes.json()

      // --- Step 2: Upload video directly to R2 ---
      // Progress 0-90% maps to the R2 upload
      await uploadToR2(presign.upload_url, file, file.type || 'video/mp4', (percent) => {
        setUploadProgress(Math.round(percent * 0.9))
      })

      // Upload complete — switch to processing phase
      setUploadProgress(90)

      // --- Step 3: Trigger analysis with video_key ---
      // Re-fetch token in case upload was slow and original token expired
      const freshToken = await getAuthToken()
      const analyzeHeaders: Record<string, string> = {}
      if (freshToken) {
        analyzeHeaders['Authorization'] = `Bearer ${freshToken}`
      }

      const analyzeForm = new FormData()
      analyzeForm.append('video_key', presign.object_key)
      const backendJumpType = jumpType === 'dropjump' ? 'drop_jump' : jumpType
      analyzeForm.append('jump_type', backendJumpType)
      analyzeForm.append('debug', enableDebug ? 'true' : 'false')
      if (sex) analyzeForm.append('sex', sex)
      if (age !== null) analyzeForm.append('age', String(age))
      if (trainingLevel) analyzeForm.append('training_level', trainingLevel)

      const analyzeRes = await fetch(getApiUrl('/api/analyze'), {
        method: 'POST',
        headers: analyzeHeaders,
        body: analyzeForm,
      })

      setUploadProgress(100)

      if (!analyzeRes.ok) {
        const errBody = await analyzeRes.json().catch(() => null)
        const errorMessage =
          errBody?.error || errBody?.message || errBody?.detail || `Server error: ${analyzeRes.status}`
        throw new Error(errorMessage)
      }

      const response: AnalysisResponse = await analyzeRes.json()
      setMetrics(response)
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error occurred'
      setError(errorMessage)
      console.error('Analysis error:', err)
    } finally {
      setLoading(false)
      setUploadProgress(0)
    }
  }

  const retry = async () => {
    if (file) {
      await analyze()
    }
  }

  const reset = () => {
    setFile(null)
    setJumpType('cmj')
    setLoading(false)
    setUploadProgress(0)
    setMetrics(null)
    setError(null)
    setEnableDebug(false)
    setSex(null)
    setAge(null)
    setTrainingLevel(null)
  }

  return {
    // State
    file,
    jumpType,
    loading,
    uploadProgress,
    metrics,
    error,
    enableDebug,
    sex,
    age,
    trainingLevel,
    // Actions
    setFile,
    setJumpType,
    setEnableDebug,
    setSex,
    setAge,
    setTrainingLevel,
    analyze,
    retry,
    reset,
  }
}
