"""Configure CORS on the R2 bucket for direct browser uploads.

WARNING: This script includes localhost origins and is intended for
development / staging environments. For production, remove the localhost
origins or use the Cloudflare Dashboard to set a production-only policy.

This script sets the CORS policy on the Kinemotion R2 bucket so that
the frontend can PUT video files directly via presigned URLs.

Usage:
    uv run python scripts/configure_r2_cors.py

Requires the same R2 env vars used by the backend:
    R2_ENDPOINT, R2_ACCESS_KEY, R2_SECRET_KEY, R2_BUCKET_NAME

Manual dashboard alternative (Cloudflare Dashboard):
    1. Go to R2 > kinemotion bucket > Settings > CORS Policy
    2. Add a rule:
       - Allowed Origins: https://kinemotion.vercel.app, http://localhost:5173
       - Allowed Methods: PUT
       - Allowed Headers: Content-Type
       - Expose Headers: ETag
       - Max Age: 3600
"""

import os
import sys

import boto3


def main() -> None:
    endpoint = os.getenv("R2_ENDPOINT", "")
    access_key = os.getenv("R2_ACCESS_KEY", "")
    secret_key = os.getenv("R2_SECRET_KEY", "")
    bucket_name = os.getenv("R2_BUCKET_NAME", "kinemotion")

    if not all([endpoint, access_key, secret_key]):
        print(
            "Error: Set R2_ENDPOINT, R2_ACCESS_KEY, and R2_SECRET_KEY environment variables.",
            file=sys.stderr,
        )
        sys.exit(1)

    client = boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name="auto",
    )

    cors_config = {
        "CORSRules": [
            {
                "AllowedOrigins": [
                    "https://kinemotion.vercel.app",
                    "http://localhost:5173",
                    "http://localhost:3000",
                ],
                "AllowedMethods": ["PUT"],
                "AllowedHeaders": ["Content-Type"],
                "ExposeHeaders": ["ETag"],
                "MaxAgeSeconds": 3600,
            }
        ]
    }

    client.put_bucket_cors(Bucket=bucket_name, CORSConfiguration=cors_config)
    print(f"CORS configured on bucket '{bucket_name}':")
    for rule in cors_config["CORSRules"]:
        print(f"  Origins: {rule['AllowedOrigins']}")
        print(f"  Methods: {rule['AllowedMethods']}")
        print(f"  Headers: {rule['AllowedHeaders']}")


if __name__ == "__main__":
    main()
