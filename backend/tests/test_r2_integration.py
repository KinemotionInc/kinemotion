"""R2 storage integration tests (mocked)."""

from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from kinemotion_backend.models import R2StorageClient


def test_r2_client_initialization_with_credentials() -> None:
    """Test R2 client initialization with valid credentials."""
    with patch.dict(
        "os.environ",
        {
            "R2_ENDPOINT": "https://r2.example.com",
            "R2_ACCESS_KEY": "test_key",
            "R2_SECRET_KEY": "test_secret",
            "R2_BUCKET_NAME": "kinemotion",
        },
    ):
        client = R2StorageClient()

        assert client.endpoint == "https://r2.example.com"
        assert client.access_key == "test_key"
        assert client.secret_key == "test_secret"
        assert client.bucket_name == "kinemotion"
        assert client.public_base_url == ""
        assert client.presign_expiration_s == 604800  # 7 days default


def test_r2_client_initialization_with_public_url() -> None:
    """Test R2 client initialization with public base URL."""
    with patch.dict(
        "os.environ",
        {
            "R2_ENDPOINT": "https://r2.example.com",
            "R2_ACCESS_KEY": "test_key",
            "R2_SECRET_KEY": "test_secret",
            "R2_PUBLIC_BASE_URL": "https://kinemotion-public.example.com",
        },
    ):
        client = R2StorageClient()

        assert client.public_base_url == "https://kinemotion-public.example.com"


def test_r2_client_initialization_strips_trailing_slash_from_public_url() -> None:
    """Test that trailing slash is stripped from public base URL."""
    with patch.dict(
        "os.environ",
        {
            "R2_ENDPOINT": "https://r2.example.com",
            "R2_ACCESS_KEY": "test_key",
            "R2_SECRET_KEY": "test_secret",
            "R2_PUBLIC_BASE_URL": "https://kinemotion-public.example.com/",
        },
    ):
        client = R2StorageClient()

        assert client.public_base_url == "https://kinemotion-public.example.com"


def test_r2_client_initialization_custom_presign_expiration() -> None:
    """Test R2 client initialization with custom presigned expiration."""
    with patch.dict(
        "os.environ",
        {
            "R2_ENDPOINT": "https://r2.example.com",
            "R2_ACCESS_KEY": "test_key",
            "R2_SECRET_KEY": "test_secret",
            "R2_PRESIGN_EXPIRATION_S": "86400",  # 1 day
        },
    ):
        client = R2StorageClient()

        assert client.presign_expiration_s == 86400


def test_r2_client_initialization_invalid_presign_expiration() -> None:
    """Test R2 client falls back to default with invalid expiration."""
    with patch.dict(
        "os.environ",
        {
            "R2_ENDPOINT": "https://r2.example.com",
            "R2_ACCESS_KEY": "test_key",
            "R2_SECRET_KEY": "test_secret",
            "R2_PRESIGN_EXPIRATION_S": "not_a_number",
        },
    ):
        client = R2StorageClient()

        assert client.presign_expiration_s == 604800  # Falls back to 7 days


def test_r2_client_initialization_missing_endpoint() -> None:
    """Test R2 client initialization fails without endpoint."""
    with patch.dict(
        "os.environ",
        {
            "R2_ENDPOINT": "",
            "R2_ACCESS_KEY": "test_key",
            "R2_SECRET_KEY": "test_secret",
        },
        clear=False,
    ):
        with pytest.raises(ValueError) as exc_info:
            R2StorageClient()

        assert "R2 credentials not configured" in str(exc_info.value)


def test_r2_client_initialization_missing_access_key() -> None:
    """Test R2 client initialization fails without access key."""
    with patch.dict(
        "os.environ",
        {
            "R2_ENDPOINT": "https://r2.example.com",
            "R2_ACCESS_KEY": "",
            "R2_SECRET_KEY": "test_secret",
        },
        clear=False,
    ):
        with pytest.raises(ValueError):
            R2StorageClient()


def test_r2_client_initialization_missing_secret_key() -> None:
    """Test R2 client initialization fails without secret key."""
    with patch.dict(
        "os.environ",
        {
            "R2_ENDPOINT": "https://r2.example.com",
            "R2_ACCESS_KEY": "test_key",
            "R2_SECRET_KEY": "",
        },
        clear=False,
    ):
        with pytest.raises(ValueError):
            R2StorageClient()


def test_r2_upload_file_success() -> None:
    """Test successful R2 file upload."""
    with patch.dict(
        "os.environ",
        {
            "R2_ENDPOINT": "https://r2.example.com",
            "R2_ACCESS_KEY": "test_key",
            "R2_SECRET_KEY": "test_secret",
        },
    ):
        with patch("kinemotion_backend.models.storage.boto3.client") as mock_boto3:
            mock_s3 = MagicMock()
            mock_boto3.return_value = mock_s3
            mock_s3.generate_presigned_url.return_value = "https://r2.example.com/presigned-url"

            client = R2StorageClient()
            url = client.upload_file("/tmp/test.mp4", "videos/test.mp4")

            mock_s3.upload_file.assert_called_once_with(
                "/tmp/test.mp4", "test-bucket", "videos/test.mp4"
            )
            mock_s3.generate_presigned_url.assert_called_once_with(
                "get_object",
                Params={"Bucket": "test-bucket", "Key": "videos/test.mp4"},
                ExpiresIn=604800,  # 7 days default
            )
            assert url == "https://r2.example.com/presigned-url"


def test_get_object_url_with_public_base_url() -> None:
    """Test that get_object_url returns public URL when configured."""
    with patch.dict(
        "os.environ",
        {
            "R2_ENDPOINT": "https://r2.example.com",
            "R2_ACCESS_KEY": "test_key",
            "R2_SECRET_KEY": "test_secret",
            "R2_PUBLIC_BASE_URL": "https://kinemotion-public.example.com",
        },
    ):
        with patch("kinemotion_backend.models.storage.boto3.client"):
            client = R2StorageClient()
            url = client.get_object_url("videos/test.mp4")

            assert url == "https://kinemotion-public.example.com/videos/test.mp4"


def test_get_object_url_without_public_base_url() -> None:
    """Test that get_object_url falls back to presigned URL when no public base."""
    with patch.dict(
        "os.environ",
        {
            "R2_ENDPOINT": "https://r2.example.com",
            "R2_ACCESS_KEY": "test_key",
            "R2_SECRET_KEY": "test_secret",
        },
    ):
        with patch("kinemotion_backend.models.storage.boto3.client") as mock_boto3:
            mock_s3 = MagicMock()
            mock_boto3.return_value = mock_s3
            mock_s3.generate_presigned_url.return_value = (
                "https://r2.example.com/presigned-url?expires=123"
            )

            client = R2StorageClient()
            url = client.get_object_url("videos/test.mp4")

            # Should call generate_presigned_url with default expiration
            mock_s3.generate_presigned_url.assert_called_once_with(
                "get_object",
                Params={"Bucket": "test-bucket", "Key": "videos/test.mp4"},
                ExpiresIn=604800,  # 7 days
            )
            assert url == "https://r2.example.com/presigned-url?expires=123"


def test_get_object_url_strips_leading_slash() -> None:
    """Test that get_object_url normalizes keys by stripping leading slash."""
    with patch.dict(
        "os.environ",
        {
            "R2_ENDPOINT": "https://r2.example.com",
            "R2_ACCESS_KEY": "test_key",
            "R2_SECRET_KEY": "test_secret",
            "R2_PUBLIC_BASE_URL": "https://kinemotion-public.example.com",
        },
    ):
        with patch("kinemotion_backend.models.storage.boto3.client"):
            client = R2StorageClient()
            url = client.get_object_url("/videos/test.mp4")  # Leading slash

            # Should strip leading slash
            assert url == "https://kinemotion-public.example.com/videos/test.mp4"


def test_get_object_url_with_custom_expiration() -> None:
    """Test that get_object_url respects custom presigned expiration."""
    with patch.dict(
        "os.environ",
        {
            "R2_ENDPOINT": "https://r2.example.com",
            "R2_ACCESS_KEY": "test_key",
            "R2_SECRET_KEY": "test_secret",
            "R2_PRESIGN_EXPIRATION_S": "3600",  # 1 hour
        },
    ):
        with patch("kinemotion_backend.models.storage.boto3.client") as mock_boto3:
            mock_s3 = MagicMock()
            mock_boto3.return_value = mock_s3
            mock_s3.generate_presigned_url.return_value = "https://r2.example.com/presigned"

            client = R2StorageClient()
            url = client.get_object_url("videos/test.mp4")

            # Should use custom expiration
            mock_s3.generate_presigned_url.assert_called_once_with(
                "get_object",
                Params={"Bucket": "test-bucket", "Key": "videos/test.mp4"},
                ExpiresIn=3600,  # Custom expiration
            )
            assert url == "https://r2.example.com/presigned"


def test_r2_upload_file_returns_url() -> None:
    """Test that R2 upload returns proper URL."""
    with patch.dict(
        "os.environ",
        {
            "R2_ENDPOINT": "https://r2.example.com",
            "R2_ACCESS_KEY": "test_key",
            "R2_SECRET_KEY": "test_secret",
        },
    ):
        with patch("kinemotion_backend.models.storage.boto3.client") as mock_boto3:
            mock_s3 = MagicMock()
            mock_boto3.return_value = mock_s3
            presigned_url = "https://r2.example.com/presigned-url"
            mock_s3.generate_presigned_url.return_value = presigned_url

            client = R2StorageClient()
            url = client.upload_file("/tmp/test.mp4", "videos/test.mp4")

            assert url == presigned_url


def test_r2_upload_file_error_handling() -> None:
    """Test R2 upload error handling."""
    with patch.dict(
        "os.environ",
        {
            "R2_ENDPOINT": "https://r2.example.com",
            "R2_ACCESS_KEY": "test_key",
            "R2_SECRET_KEY": "test_secret",
        },
    ):
        with patch("kinemotion_backend.models.storage.boto3.client") as mock_boto3:
            mock_s3 = MagicMock()
            mock_s3.upload_file.side_effect = Exception("Upload failed")
            mock_boto3.return_value = mock_s3

            client = R2StorageClient()

            with pytest.raises(IOError) as exc_info:
                client.upload_file("/tmp/test.mp4", "videos/test.mp4")

            assert "Failed to upload to R2" in str(exc_info.value)


def test_r2_download_file_success() -> None:
    """Test successful R2 file download."""
    with patch.dict(
        "os.environ",
        {
            "R2_ENDPOINT": "https://r2.example.com",
            "R2_ACCESS_KEY": "test_key",
            "R2_SECRET_KEY": "test_secret",
        },
    ):
        with patch("kinemotion_backend.models.storage.boto3.client") as mock_boto3:
            mock_s3 = MagicMock()
            mock_boto3.return_value = mock_s3

            client = R2StorageClient()
            client.download_file("videos/test.mp4", "/tmp/test.mp4")

            mock_s3.download_file.assert_called_once_with(
                "test-bucket", "videos/test.mp4", "/tmp/test.mp4"
            )


def test_r2_download_file_error_handling() -> None:
    """Test R2 download error handling."""
    with patch.dict(
        "os.environ",
        {
            "R2_ENDPOINT": "https://r2.example.com",
            "R2_ACCESS_KEY": "test_key",
            "R2_SECRET_KEY": "test_secret",
        },
    ):
        with patch("kinemotion_backend.models.storage.boto3.client") as mock_boto3:
            mock_s3 = MagicMock()
            mock_s3.download_file.side_effect = Exception("Download failed")
            mock_boto3.return_value = mock_s3

            client = R2StorageClient()

            with pytest.raises(IOError) as exc_info:
                client.download_file("videos/test.mp4", "/tmp/test.mp4")

            assert "Failed to download from R2" in str(exc_info.value)


def test_r2_delete_file_success() -> None:
    """Test successful R2 file deletion."""
    with patch.dict(
        "os.environ",
        {
            "R2_ENDPOINT": "https://r2.example.com",
            "R2_ACCESS_KEY": "test_key",
            "R2_SECRET_KEY": "test_secret",
        },
    ):
        with patch("kinemotion_backend.models.storage.boto3.client") as mock_boto3:
            mock_s3 = MagicMock()
            mock_boto3.return_value = mock_s3

            client = R2StorageClient()
            client.delete_file("videos/test.mp4")

            mock_s3.delete_object.assert_called_once_with(
                Bucket="test-bucket", Key="videos/test.mp4"
            )


def test_r2_delete_file_error_handling() -> None:
    """Test R2 deletion error handling."""
    with patch.dict(
        "os.environ",
        {
            "R2_ENDPOINT": "https://r2.example.com",
            "R2_ACCESS_KEY": "test_key",
            "R2_SECRET_KEY": "test_secret",
        },
    ):
        with patch("kinemotion_backend.models.storage.boto3.client") as mock_boto3:
            mock_s3 = MagicMock()
            mock_s3.delete_object.side_effect = Exception("Delete failed")
            mock_boto3.return_value = mock_s3

            client = R2StorageClient()

            with pytest.raises(IOError) as exc_info:
                client.delete_file("videos/test.mp4")

            assert "Failed to delete from R2" in str(exc_info.value)


def test_r2_put_object_success() -> None:
    """Test successful R2 put object (for results)."""
    with patch.dict(
        "os.environ",
        {
            "R2_ENDPOINT": "https://r2.example.com",
            "R2_ACCESS_KEY": "test_key",
            "R2_SECRET_KEY": "test_secret",
        },
    ):
        with patch("kinemotion_backend.models.storage.boto3.client") as mock_boto3:
            mock_s3 = MagicMock()
            mock_boto3.return_value = mock_s3
            mock_s3.generate_presigned_url.return_value = "https://r2.example.com/presigned-url"

            client = R2StorageClient()
            url = client.put_object("results/test.json", b'{"status": "ok"}')

            mock_s3.put_object.assert_called_once()
            mock_s3.generate_presigned_url.assert_called_once_with(
                "get_object",
                Params={"Bucket": "test-bucket", "Key": "results/test.json"},
                ExpiresIn=604800,  # 7 days default
            )
            assert url == "https://r2.example.com/presigned-url"


def test_r2_put_object_error_handling() -> None:
    """Test R2 put object error handling."""
    with patch.dict(
        "os.environ",
        {
            "R2_ENDPOINT": "https://r2.example.com",
            "R2_ACCESS_KEY": "test_key",
            "R2_SECRET_KEY": "test_secret",
        },
    ):
        with patch("kinemotion_backend.models.storage.boto3.client") as mock_boto3:
            mock_s3 = MagicMock()
            mock_s3.put_object.side_effect = Exception("Put failed")
            mock_boto3.return_value = mock_s3

            client = R2StorageClient()

            with pytest.raises(IOError) as exc_info:
                client.put_object("results/test.json", b'{"status": "ok"}')

            assert "Failed to put object to R2" in str(exc_info.value)


def test_generate_presigned_upload_url_success() -> None:
    """Test successful presigned upload URL generation."""
    with patch.dict(
        "os.environ",
        {
            "R2_ENDPOINT": "https://r2.example.com",
            "R2_ACCESS_KEY": "test_key",
            "R2_SECRET_KEY": "test_secret",
        },
    ):
        with patch("kinemotion_backend.models.storage.boto3.client") as mock_boto3:
            mock_s3 = MagicMock()
            mock_boto3.return_value = mock_s3
            mock_s3.generate_presigned_url.return_value = (
                "https://r2.example.com/presigned-put-url"
            )

            client = R2StorageClient()
            url = client.generate_presigned_upload_url("videos/uploads/test.mp4", "video/mp4")

            mock_s3.generate_presigned_url.assert_called_once_with(
                "put_object",
                Params={
                    "Bucket": "test-bucket",
                    "Key": "videos/uploads/test.mp4",
                    "ContentType": "video/mp4",
                },
                ExpiresIn=900,
            )
            assert url == "https://r2.example.com/presigned-put-url"


def test_generate_presigned_upload_url_custom_expiration() -> None:
    """Test presigned upload URL with custom expiration."""
    with patch.dict(
        "os.environ",
        {
            "R2_ENDPOINT": "https://r2.example.com",
            "R2_ACCESS_KEY": "test_key",
            "R2_SECRET_KEY": "test_secret",
        },
    ):
        with patch("kinemotion_backend.models.storage.boto3.client") as mock_boto3:
            mock_s3 = MagicMock()
            mock_boto3.return_value = mock_s3
            mock_s3.generate_presigned_url.return_value = "https://r2.example.com/url"

            client = R2StorageClient()
            client.generate_presigned_upload_url("videos/test.mp4", "video/mp4", expiration=1800)

            call_kwargs = mock_s3.generate_presigned_url.call_args
            assert call_kwargs[1]["ExpiresIn"] == 1800


def test_generate_presigned_upload_url_content_type() -> None:
    """Test presigned upload URL passes content type correctly."""
    with patch.dict(
        "os.environ",
        {
            "R2_ENDPOINT": "https://r2.example.com",
            "R2_ACCESS_KEY": "test_key",
            "R2_SECRET_KEY": "test_secret",
        },
    ):
        with patch("kinemotion_backend.models.storage.boto3.client") as mock_boto3:
            mock_s3 = MagicMock()
            mock_boto3.return_value = mock_s3
            mock_s3.generate_presigned_url.return_value = "https://r2.example.com/url"

            client = R2StorageClient()
            client.generate_presigned_upload_url("videos/test.mov", "video/quicktime")

            call_kwargs = mock_s3.generate_presigned_url.call_args
            assert call_kwargs[1]["Params"]["ContentType"] == "video/quicktime"


def test_generate_presigned_upload_url_error_handling() -> None:
    """Test presigned upload URL error handling."""
    with patch.dict(
        "os.environ",
        {
            "R2_ENDPOINT": "https://r2.example.com",
            "R2_ACCESS_KEY": "test_key",
            "R2_SECRET_KEY": "test_secret",
        },
    ):
        with patch("kinemotion_backend.models.storage.boto3.client") as mock_boto3:
            mock_s3 = MagicMock()
            mock_s3.generate_presigned_url.side_effect = Exception("Presign failed")
            mock_boto3.return_value = mock_s3

            client = R2StorageClient()

            with pytest.raises(IOError) as exc_info:
                client.generate_presigned_upload_url("videos/test.mp4", "video/mp4")

            assert "Failed to generate presigned upload URL" in str(exc_info.value)


def test_r2_bucket_name_from_env() -> None:
    """Test that R2 bucket name is read from environment."""
    with patch.dict(
        "os.environ",
        {
            "R2_ENDPOINT": "https://r2.example.com",
            "R2_ACCESS_KEY": "test_key",
            "R2_SECRET_KEY": "test_secret",
            "R2_BUCKET_NAME": "custom-bucket",
        },
    ):
        client = R2StorageClient()
        assert client.bucket_name == "custom-bucket"


def test_r2_bucket_name_default() -> None:
    """Test that R2 bucket name defaults to 'kinemotion'."""
    with patch.dict(
        "os.environ",
        {
            "R2_ENDPOINT": "https://r2.example.com",
            "R2_ACCESS_KEY": "test_key",
            "R2_SECRET_KEY": "test_secret",
            "R2_BUCKET_NAME": "",
        },
        clear=False,
    ):
        client = R2StorageClient()
        assert client.bucket_name == "kinemotion"


def test_r2_client_initialization_region_auto() -> None:
    """Test that R2 client uses 'auto' region."""
    with patch.dict(
        "os.environ",
        {
            "R2_ENDPOINT": "https://r2.example.com",
            "R2_ACCESS_KEY": "test_key",
            "R2_SECRET_KEY": "test_secret",
        },
    ):
        with patch("kinemotion_backend.models.storage.boto3.client") as mock_boto3:
            R2StorageClient()

            # Verify boto3 was called with region_name="auto"
            call_kwargs = mock_boto3.call_args[1]
            assert call_kwargs.get("region_name") == "auto"


def test_multiple_r2_operations_sequential() -> None:
    """Test multiple R2 operations in sequence."""
    with patch.dict(
        "os.environ",
        {
            "R2_ENDPOINT": "https://r2.example.com",
            "R2_ACCESS_KEY": "test_key",
            "R2_SECRET_KEY": "test_secret",
        },
    ):
        with patch("kinemotion_backend.models.storage.boto3.client") as mock_boto3:
            mock_s3 = MagicMock()
            mock_boto3.return_value = mock_s3

            client = R2StorageClient()

            # Upload
            client.upload_file("/tmp/test.mp4", "videos/test.mp4")
            # Put object
            client.put_object("results/test.json", b'{"status": "ok"}')
            # Delete
            client.delete_file("videos/test.mp4")

            # Verify all operations were called
            assert mock_s3.upload_file.called
            assert mock_s3.put_object.called
            assert mock_s3.delete_object.called


# --- Service-level tests for AnalysisService.analyze_from_r2_key ---


async def test_analyze_from_r2_key_success(
    sample_cmj_metrics: dict[str, Any],
) -> None:
    """Test analyze_from_r2_key downloads from R2, processes, and returns response."""
    from kinemotion_backend.services.analysis_service import AnalysisService

    service = AnalysisService()

    # Mock storage service: download_file writes a dummy temp file
    def fake_download(key: str, dest: str) -> None:
        with open(dest, "wb") as f:
            f.write(b"\x00" * 1024)  # 1KB dummy file

    service.storage_service.client.download_file = MagicMock(side_effect=fake_download)
    service.storage_service.client.get_object_url = MagicMock(
        return_value="https://r2.example.com/videos/test.mp4"
    )
    service.storage_service.get_temp_file_path = MagicMock(
        return_value="/tmp/test_r2_download.mp4"
    )

    # Mock upload methods
    service.storage_service.upload_analysis_results = AsyncMock(
        return_value="https://r2.example.com/results/test.json"
    )
    service.storage_service.upload_video = AsyncMock(
        return_value="https://r2.example.com/debug/test.mp4"
    )

    # Mock video processor
    class MockCMJResult:
        def to_dict(self) -> dict[str, Any]:
            return sample_cmj_metrics

    with patch("kinemotion_backend.services.analysis_service.process_cmj_video") as mock_cmj:
        mock_cmj.return_value = MockCMJResult()

        result = await service.analyze_from_r2_key(
            video_key="videos/uploads/test@example.com/2026/03/03/abc.mp4",
            jump_type="cmj",
            quality="balanced",
        )

    assert result.status_code == 200
    assert result.message == "Analysis completed successfully"
    assert result.metrics is not None

    # Verify R2 download was called with the correct key
    service.storage_service.client.download_file.assert_called_once()
    call_args = service.storage_service.client.download_file.call_args[0]
    assert call_args[0] == "videos/uploads/test@example.com/2026/03/03/abc.mp4"


async def test_analyze_from_r2_key_download_failure() -> None:
    """Test analyze_from_r2_key handles R2 download failure gracefully."""
    from kinemotion_backend.services.analysis_service import AnalysisService

    service = AnalysisService()

    service.storage_service.client.download_file = MagicMock(
        side_effect=OSError("Failed to download from R2")
    )
    service.storage_service.get_temp_file_path = MagicMock(
        return_value="/tmp/test_r2_download.mp4"
    )

    result = await service.analyze_from_r2_key(
        video_key="videos/uploads/test@example.com/2026/03/03/abc.mp4",
        jump_type="cmj",
    )

    assert result.status_code == 500
    assert "Analysis failed" in result.message
