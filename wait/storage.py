"""Custom static files storage."""

from whitenoise.storage import CompressedManifestStaticFilesStorage


class ManifestStaticFilesStorage(CompressedManifestStaticFilesStorage):
    """Compressed, cache-busted static files.

    ``manifest_strict`` is disabled so that development and test runs (where
    ``collectstatic`` has not been executed yet) fall back to the original
    filenames instead of raising ``ValueError``.
    """

    manifest_strict = False

    def hashed_name(self, name, content=None, filename=None):
        """Fall back to the original name when the file is missing.

        Without this, rendering templates in tests (or before the first
        ``collectstatic`` run) fails because no manifest exists yet.
        """
        try:
            return super().hashed_name(name, content, filename)
        except ValueError:
            return name
