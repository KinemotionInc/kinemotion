import { renderHook, act, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { useAnalysis } from './useAnalysis';

// Mock Supabase
vi.mock('../lib/supabase', () => ({
  supabase: {
    auth: {
      getSession: vi.fn().mockResolvedValue({ data: { session: { access_token: 'mock-token' } } }),
    },
  },
}));

describe('useAnalysis Hook', () => {
  let mockXHR: any;

  beforeEach(() => {
    vi.clearAllMocks();

    // Mock XMLHttpRequest for R2 upload (step 2)
    mockXHR = {
      open: vi.fn(),
      send: vi.fn(),
      setRequestHeader: vi.fn(),
      upload: {
        addEventListener: vi.fn(),
      },
      addEventListener: vi.fn(),
      status: 200,
      responseText: '',
    };

    class MockXMLHttpRequest {
      open(...args: any[]) { return mockXHR.open(...args); }
      send(...args: any[]) { return mockXHR.send(...args); }
      setRequestHeader(...args: any[]) { return mockXHR.setRequestHeader(...args); }
      get upload() { return mockXHR.upload; }
      addEventListener(...args: any[]) { return mockXHR.addEventListener(...args); }
      get status() { return mockXHR.status; }
      set status(v) { mockXHR.status = v; }
      get responseText() { return mockXHR.responseText; }
      set responseText(v) { mockXHR.responseText = v; }
    }

    vi.stubGlobal('XMLHttpRequest', MockXMLHttpRequest);
  });

  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it('should initialize with default state', () => {
    const { result } = renderHook(() => useAnalysis());

    expect(result.current.file).toBeNull();
    expect(result.current.jumpType).toBe('cmj');
    expect(result.current.loading).toBe(false);
    expect(result.current.metrics).toBeNull();
    expect(result.current.error).toBeNull();
    expect(result.current.uploadProgress).toBe(0);
  });

  it('should set file and jump type', () => {
    const { result } = renderHook(() => useAnalysis());
    const file = new File(['dummy content'], 'test.mp4', { type: 'video/mp4' });

    act(() => {
      result.current.setFile(file);
      result.current.setJumpType('dropjump');
    });

    expect(result.current.file).toBe(file);
    expect(result.current.jumpType).toBe('dropjump');
  });

  it('should show error if analyze is called without a file', async () => {
    const { result } = renderHook(() => useAnalysis());

    await act(async () => {
      await result.current.analyze();
    });

    expect(result.current.error).toBe('Please select a video file');
    expect(result.current.loading).toBe(false);
  });

  it('should reject files over 200MB', async () => {
    const { result } = renderHook(() => useAnalysis());
    // Create a File-like object with size > 200MB
    const bigFile = new File([], 'big.mp4', { type: 'video/mp4' });
    Object.defineProperty(bigFile, 'size', { value: 201 * 1024 * 1024 });

    act(() => {
      result.current.setFile(bigFile);
    });

    await act(async () => {
      await result.current.analyze();
    });

    expect(result.current.error).toBe('Video file is too large. Maximum size is 200MB.');
    expect(result.current.loading).toBe(false);
  });

  it('should handle successful three-step analysis flow', async () => {
    const mockAnalysisResponse = {
      status: 200,
      message: 'Success',
      metrics: { data: { jump_height_m: 0.5 } },
    };

    // Mock fetch for step 1 (presign) and step 3 (analyze)
    let fetchCallCount = 0;
    const mockFetch = vi.fn().mockImplementation(() => {
      fetchCallCount++;
      if (fetchCallCount === 1) {
        // Step 1: presign response
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve({
            upload_url: 'https://r2.example.com/presigned-put',
            object_key: 'videos/uploads/test.mp4',
            expires_in: 900,
          }),
        });
      } else {
        // Step 3: analyze response
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockAnalysisResponse),
        });
      }
    });
    vi.stubGlobal('fetch', mockFetch);

    // Mock XHR for step 2 (R2 upload) — auto-resolve on send
    const xhrEventListeners: Record<string, EventListener> = {};
    mockXHR.addEventListener.mockImplementation((event: string, cb: EventListener) => {
      xhrEventListeners[event] = cb;
    });
    mockXHR.send.mockImplementation(() => {
      mockXHR.status = 200;
      // Simulate immediate success
      setTimeout(() => {
        if (xhrEventListeners['load']) {
          xhrEventListeners['load']({} as Event);
        }
      }, 0);
    });

    const { result } = renderHook(() => useAnalysis());
    const file = new File(['dummy content'], 'test.mp4', { type: 'video/mp4' });

    act(() => {
      result.current.setFile(file);
    });

    await act(async () => {
      await result.current.analyze();
    });

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    expect(result.current.metrics).toEqual(mockAnalysisResponse);
    expect(result.current.error).toBeNull();

    // Verify presign fetch was called
    expect(mockFetch).toHaveBeenCalledTimes(2);
    // Step 1: presign
    expect(mockFetch.mock.calls[0][0]).toContain('/api/upload/presign');
    // Step 3: analyze
    expect(mockFetch.mock.calls[1][0]).toContain('/api/analyze');

    // Verify XHR was used for R2 upload
    expect(mockXHR.open).toHaveBeenCalledWith('PUT', 'https://r2.example.com/presigned-put');
  });

  it('should handle presign API error', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 500,
      json: () => Promise.resolve({ detail: 'Internal server error' }),
    });
    vi.stubGlobal('fetch', mockFetch);

    const { result } = renderHook(() => useAnalysis());
    const file = new File(['dummy content'], 'test.mp4', { type: 'video/mp4' });

    act(() => {
      result.current.setFile(file);
    });

    await act(async () => {
      await result.current.analyze();
    });

    expect(result.current.error).toBe('Internal server error');
    expect(result.current.loading).toBe(false);
    expect(result.current.metrics).toBeNull();
  });

  it('should handle R2 upload network error', async () => {
    // Step 1 (presign) succeeds
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({
        upload_url: 'https://r2.example.com/presigned-put',
        object_key: 'videos/test.mp4',
        expires_in: 900,
      }),
    });
    vi.stubGlobal('fetch', mockFetch);

    // Step 2 (R2 upload) fails with network error
    const xhrEventListeners: Record<string, EventListener> = {};
    mockXHR.addEventListener.mockImplementation((event: string, cb: EventListener) => {
      xhrEventListeners[event] = cb;
    });
    mockXHR.send.mockImplementation(() => {
      setTimeout(() => {
        if (xhrEventListeners['error']) {
          xhrEventListeners['error']({} as Event);
        }
      }, 0);
    });

    const { result } = renderHook(() => useAnalysis());
    const file = new File(['dummy content'], 'test.mp4', { type: 'video/mp4' });

    act(() => {
      result.current.setFile(file);
    });

    await act(async () => {
      await result.current.analyze();
    });

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    expect(result.current.error).toBe('Network error: Unable to upload video');
  });

  it('should reset state', () => {
    const { result } = renderHook(() => useAnalysis());

    act(() => {
      result.current.setFile(new File([], 'test.mp4'));
      result.current.setJumpType('dropjump');
      result.current.setEnableDebug(true);
    });

    expect(result.current.file).not.toBeNull();
    expect(result.current.jumpType).toBe('dropjump');
    expect(result.current.enableDebug).toBe(true);

    act(() => {
      result.current.reset();
    });

    expect(result.current.file).toBeNull();
    expect(result.current.jumpType).toBe('cmj');
    expect(result.current.enableDebug).toBe(false);
    expect(result.current.error).toBeNull();
    expect(result.current.metrics).toBeNull();
  });
});
