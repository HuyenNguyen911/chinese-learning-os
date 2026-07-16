#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audio_manifest.py — Liệt kê các job TTS (text -> file -> voice) từ baitap spec.

KHÔNG gọi mạng. Việc sinh MP3 thật (edge-tts) là bước riêng, có cổng xác nhận
của user (xem SKILL.md). Đây chỉ là phần lập kế hoạch, kiểm thử được.
"""

DEFAULT_VOICE = "zh-CN-XiaoxiaoNeural"


def build_audio_manifest(spec, voice=DEFAULT_VOICE):
    jobs = []
    for block in spec.get("blocks", []):
        if block.get("type") not in ("nghe", "noi_hskk"):
            continue
        for it in block.get("items", []):
            path = it.get("audio")
            if not path:
                continue
            jobs.append({"text": it.get("script", ""), "file": path,
                         "voice": voice})
    return jobs
