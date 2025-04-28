import sys
import os
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional

# 添加src目录到Python路径
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def download_bilibili_video(url: str, output_dir: str = "./downloads", batch: bool = False, episodes: Optional[str] = None, **kwargs: Any) -> None:
    """
    下载B站视频的函数 - 使用yutto库实现

    参数:
    url: str - 视频URL，支持多种格式：
        - 普通视频：https://www.bilibili.com/video/BV1xH5jzVEs2
        - 合集：https://space.bilibili.com/11336264/channel/collectiondetail?sid=26634
        - 番剧：https://www.bilibili.com/bangumi/play/ss26801
        - 课程：https://www.bilibili.com/cheese/play/ss205
        - 收藏夹：https://space.bilibili.com/11336264/favlist?fid=75458
        - 视频列表：https://space.bilibili.com/11336264/channel/seriesdetail?sid=340927
    output_dir: str - 下载目录，默认"./downloads"
    batch: bool - 是否启用批量下载模式，用于下载合集、收藏夹等，默认False
    episodes: str - 选集范围，例如"1,2,3"或"1-3"，默认下载全部

    可选参数:
    - video_quality: int - 视频质量，默认80（1080P）
      可选值:
        - 127: 8K
        - 126: Dolby Vision
        - 125: HDR
        - 120: 4K
        - 116: 1080P60
        - 112: 1080P+
        - 100: 智能修复
        - 80: 1080P
        - 74: 720P60
        - 64: 720P
        - 32: 480P
        - 16: 360P
    - audio_quality: int - 音频质量，默认30280（320kbps）
      可选值:
        - 30251: Hi-Res
        - 30255: Dolby Audio
        - 30250: Dolby Atmos
        - 30280: 320kbps
        - 30232: 128kbps
        - 30216: 64kbps
    - num_workers: int - 同时下载的线程数，默认8
    - overwrite: bool - 是否覆盖已存在的文件，默认False
    - proxy: str - 代理设置，默认"auto"
      可选值:
        - "auto": 使用系统代理
        - "no": 不使用代理
        - 其他值: 自定义代理地址，例如"http://127.0.0.1:7890"
    - sessdata: str - B站登录凭证，用于下载需要登录的视频
    - danmaku_format: str - 弹幕格式，默认"xml"
      可选值:
        - "xml": XML格式
        - "ass": ASS格式
        - "protobuf": Protobuf格式
    - vcodec: str - 视频编码格式，格式为"下载格式:生成格式"，默认"avc:copy"
      常用值:
        - "avc:copy": 下载AVC编码，保持原始编码
        - "hevc:copy": 下载HEVC编码，保持原始编码
        - "av1:copy": 下载AV1编码，保持原始编码
    - acodec: str - 音频编码格式，格式为"下载格式:生成格式"，默认"mp4a:copy"
      常用值:
        - "mp4a:copy": 下载MP4A编码，保持原始编码
        - "flac:copy": 下载FLAC编码，保持原始编码

    返回:
    None - 函数无返回值，下载结果会在控制台显示

    示例:
    # 下载单个视频
    download_bilibili_video("https://www.bilibili.com/video/BV1xH5jzVEs2")

    # 下载合集（需启用batch模式）
    download_bilibili_video(
        "https://space.bilibili.com/11336264/channel/collectiondetail?sid=26634",
        batch=True
    )

    # 下载合集中的特定视频
    download_bilibili_video(
        "https://space.bilibili.com/11336264/channel/collectiondetail?sid=26634",
        batch=True,
        episodes="1,3,5"  # 只下载第1,3,5集
    )
    """
    # 确保下载目录存在
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # 构建基本命令 - 使用当前Python解释器
    python_exe = sys.executable
    cmd: List[str] = [python_exe, "-m", "yutto", url, "--dir", output_dir]

    # 添加批量下载参数
    if batch:
        cmd.append("--batch")

    # 添加选集参数
    if episodes:
        cmd.extend(["--episodes", episodes])

    # 参数映射表 - 将Python函数参数映射到命令行参数
    param_mapping: Dict[str, str] = {
        "video_quality": "--video-quality",     # 视频质量
        "audio_quality": "--audio-quality",     # 音频质量
        "num_workers": "--num-workers",         # 下载线程数
        "danmaku_format": "--danmaku-format",   # 弹幕格式
        "proxy": "--proxy",                     # 代理设置
        "sessdata": "--sessdata",               # 登录凭证
        "vcodec": "--vcodec",                   # 视频编码
        "acodec": "--acodec"                    # 音频编码
    }

    # 添加命令行参数
    for param, cmd_param in param_mapping.items():
        if param in kwargs and kwargs[param] is not None:
            cmd.append(cmd_param)
            cmd.append(str(kwargs[param]))

    # 布尔参数特殊处理 - 仅当值为True时添加标志
    if kwargs.get("overwrite", False):
        cmd.append("--overwrite")

    # 输出执行信息
    print(f"开始下载: {url}")
    print(f"下载目录: {output_dir}")
    print(f"批量模式: {'启用' if batch else '禁用'}")
    if episodes:
        print(f"选集范围: {episodes}")
    print(f"执行命令: {' '.join(cmd)}")

    # 使用当前环境变量并添加Python路径
    env = dict(os.environ)
    env["PYTHONPATH"] = str(src_path) + ";" + env.get("PYTHONPATH", "")

    # 执行命令
    result = subprocess.run(cmd, env=env)

    # 处理执行结果
    if result.returncode == 0:
        print("下载完成!")
    else:
        print(f"下载失败，返回码: {result.returncode}")

if __name__ == "__main__":
    # 示例1: 下载单个视频
    # download_bilibili_video(
    #     "https://www.bilibili.com/video/BV1xH5jzVEs2",  # 视频URL
    #     output_dir="downloads",                         # 下载目录
    #     video_quality=112,                              # 视频质量:1080P+
    #     audio_quality=30280,                            # 音频质量:320kbps
    #     num_workers=8,                                  # 8个下载线程
    #     vcodec="avc:copy",                              # 视频编码
    #     acodec="mp4a:copy"                              # 音频编码
    # )

    # 示例2: 下载合集(取消注释以使用)
    download_bilibili_video(
        "https://space.bilibili.com/20972760/favlist?fid=1645833860&ftype=create",
        output_dir="downloads/collection",
        batch=True,                                    # 启用批量下载
        video_quality=80,                              # 视频质量:1080P
        audio_quality=30280,                           # 音频质量:320kbps
        num_workers=8                                  # 8个下载线程
    )
