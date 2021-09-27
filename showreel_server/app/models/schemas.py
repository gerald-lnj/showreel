"""
Schema definitions
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import logging
from typing import Dict, List

from pydantic import BaseModel, validator

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


class Standard(Enum):
    PAL = 25
    NTSC = 30


class Definition(Enum):
    HD = "HD"
    SD = "SD"


def timecode_math_validator(func):
    """Ensure type and Standard is the same"""

    def wrap(timecode_1: Timecode, timecode_2: Timecode):
        if not isinstance(timecode_1, Timecode):
            raise TypeError(f"{repr(timecode_1)} is not a Timecode object.")

        if not isinstance(timecode_2, Timecode):
            raise TypeError(f"{repr(timecode_2)} is not a Timecode object.")

        if timecode_1.standard != timecode_2.standard:
            raise ValueError(
                f"Standards do not match ({timecode_1.standard} and {timecode_2.standard})."
            )
        return func(timecode_1, timecode_2)

    return wrap


@dataclass
class Timecode:
    standard: Standard
    hours: int = 0
    minutes: int = 0
    seconds: int = 0
    frames: int = 0

    def __str__(self) -> str:
        return f"{self.hours:02}:{self.minutes:02}:{self.seconds:02}:{self.frames:02}"

    def __repr__(self) -> str:
        return f"{__class__.__name__}(hours={self.hours}, minutes={self.minutes}, seconds={self.seconds}, frames={self.frames}, standard={self.standard})"

    @timecode_math_validator
    def __add__(self, p2: Timecode):
        sum_frames = self.total_frames() + p2.total_frames()
        return self.from_frames(sum_frames, self.standard)

    __radd__ = __add__

    @timecode_math_validator
    def __sub__(self, p2: Timecode):
        sum_frames = self.total_frames() - p2.total_frames()
        if sum_frames < 0:
            LOG.warning(f"Subtracting a greater Timecode, Timecode of 0 returned")
            sum_frames = 0
        return Timecode.from_frames(sum_frames, self.standard)

    @timecode_math_validator
    def __eq__(self, p2: Timecode) -> bool:
        return str(self) == str(p2) and self.standard == p2.standard

    def total_frames(self) -> int:
        total_seconds = self.seconds + (self.minutes * 60) + (self.hours * 60 ** 2)
        return (total_seconds * self.standard.value) + self.frames

    @classmethod
    def from_frames(cls, total_frames: int, standard: Standard):
        total_seconds, frames = divmod(total_frames, standard.value)
        total_minutes, seconds = divmod(total_seconds, 60)
        hours, minutes = divmod(total_minutes, 60)
        return cls(
            standard=standard,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            frames=frames,
        )

    @classmethod
    def from_str(cls, timecode_str: str, standard: Standard):
        try:
            hours, minutes, seconds, frames = map(int, timecode_str.split(":"))
        except Exception:
            raise ValueError(f"{timecode_str} is not in the format HH:MM:ss:ff")
        return cls(
            standard=standard,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            frames=frames,
        )


class Clip(BaseModel):
    name: str
    description: str
    standard: Standard
    definition: Definition
    start_timecode: Timecode
    end_timecode: Timecode

    class Config:
        arbitrary_types_allowed = True

    @validator("start_timecode", "end_timecode")
    def timecode_standard(cls, v: Timecode, values: Dict):
        clip_standard: Standard = values["standard"]
        if v.standard != clip_standard:
            raise ValueError(
                f"Timecode {v} is {v.standard} but Clip {values['name']} is {clip_standard}"
            )

        return v

    @classmethod
    def from_dict(cls, *args, **kwargs):
        name: str = kwargs["name"]
        description: str = kwargs["description"]
        standard: Standard = getattr(Standard, kwargs["standard"])
        definition: Definition = Definition(kwargs["definition"])
        start_timecode = Timecode.from_str(kwargs["start_timecode"], standard)
        end_timecode = Timecode.from_str(kwargs["end_timecode"], standard)
        return cls(
            name=name,
            description=description,
            standard=standard,
            definition=definition,
            start_timecode=start_timecode,
            end_timecode=end_timecode,
        )

    def dict(self):
        """
        Override Basemodel.dict() for custom dict representation
        """
        return {
            "name": self.name,
            "description": self.description,
            "standard": self.standard.name,
            "definition": self.definition.value,
            "start_timecode": str(self.start_timecode),
            "end_timecode": str(self.end_timecode),
        }


class Reel(BaseModel):
    name: str
    standard: Standard
    definition: Definition
    clips: List[Clip]
    duration: Timecode = None

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **data):
        super().__init__(**data)
        self.duration = self.get_duration()

    @validator("clips")
    def clips_post_init(cls, v: List[Clip], values: Dict):
        """
        Validate that all clips share Standard with Reel
        """
        if len(v) == 0:
            return ValueError("At least 1 clip required.")

        reel_standard: Standard = values["standard"]
        reel_definition: Definition = values["definition"]

        current_timecode = Timecode(reel_standard)
        for clip in v:
            if clip.standard != reel_standard:
                raise ValueError(
                    f"Clip {clip.name} is {clip.standard} but Reel {values['name']} is {reel_standard}"
                )

            if clip.definition != reel_definition:
                raise ValueError(
                    f"Clip {clip.name} is {clip.definition} but Reel {values['name']} is {reel_definition}"
                )
            clip.start_timecode = current_timecode
            clip.end_timecode += current_timecode

            # current_timecode = clip.end_timecode + Timecode(reel_standard, frames=1)
            current_timecode = clip.end_timecode

        return v

    def get_duration(self) -> Timecode:
        """
        Return Timecode object that represents full duration of Reel

        Returns:
            Timecode: Total duration
        """
        # each clip's internal start_timecode is always 0
        # duration of clip is represented by end_timecode
        # first_timecode = self.clips[0].end_timecode
        # return sum([clip.end_timecode for clip in self.clips[1:]], start=first_timecode)

        return self.clips[-1].end_timecode

    def dict(self):
        """
        Override Basemodel.dict() for custom dict representation
        """
        return {
            "name": self.name,
            "standard": self.standard.name,
            "definition": self.definition.value,
            "clips": [clip.dict() for clip in self.clips],
            "duration": str(self.duration),
        }

    @classmethod
    def from_dict(cls, *args, **kwargs):
        name: str = kwargs["name"]
        standard: Standard = getattr(Standard, kwargs["standard"])
        definition: Definition = getattr(Definition, kwargs["definition"])
        clips: List[Clip] = [Clip.from_dict(**clip) for clip in kwargs["clips"]]

        return cls(name=name, standard=standard, definition=definition, clips=clips,)
