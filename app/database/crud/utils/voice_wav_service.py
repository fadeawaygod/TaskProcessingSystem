import asyncio
import base64
import tempfile
import time

import sox

from app.utils.logging.logger import get_logger

logger = get_logger()


async def get_audio_data_in_base64_in_new_thread(
    input_filepath: str,
    anchor_start: float = 0.0,
    duration: float = 0.0,
    trim_required: bool = True,
) -> str:
    """
    Run get_audio_data_in_base64_in_new_thread to prevent it from blocking the main loop.
    """
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        None,
        get_audio_data_in_base64,
        input_filepath,
        anchor_start,
        duration,
        trim_required,
    )


def get_audio_data_in_base64(
    input_filepath: str,
    anchor_start: float = 0.0,
    duration: float = 0.0,
    trim_required: bool = True,
) -> str:
    """
    Get audio data in base64 encoding.
    If trim_required is set to True, trim audio data from
        `anchor_start` (seconds) for `duration` (seconds)

    WARNING: It's a BLOCKING operation, please use a thread to run it.
    """
    logger.debug(
        (
            f"loading wav: path: {input_filepath}, anchor_start:{anchor_start}, duration:{duration}, "
            f"trim_required:{trim_required}"
        )
    )
    if trim_required:
        t1 = time.time()
        anchor_end = anchor_start + duration
        # base_name = os.path.basename(input_filepath)
        # raw_filename, file_extension = os.path.splitext(base_name)
        # Use memory as buffer up to 2MB
        with tempfile.NamedTemporaryFile(suffix=".wav", buffering=1000000) as tmp:
            wav = sox.Transformer()
            wav.trim(anchor_start, anchor_end)
            wav.build(input_filepath=input_filepath, output_filepath=tmp.name)
            t2 = time.time()
            logger.info(f"building wav takes {t2-t1} seconds")
            with open(tmp.name, "rb") as f:
                binary_file_data = f.read()
                base64_encoded_data = base64.b64encode(binary_file_data)

    else:
        with open(input_filepath, "rb") as file:
            binary_file_data = file.read()
            base64_encoded_data = base64.b64encode(binary_file_data)

    encoded_audio = base64_encoded_data.decode()
    logger.debug(f"loaded wav: path: {input_filepath}")
    return encoded_audio
