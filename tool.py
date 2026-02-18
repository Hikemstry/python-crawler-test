
"""
通用FFmpeg工具类,支持批量合并、转码、提取音频、截图、批量处理等功能。
"""
import os
import subprocess
from typing import List, Optional

class FFmpegTool:
    def __init__(self, ffmpeg_path: str = "ffmpeg"):
        self.ffmpeg_path = ffmpeg_path

    def merge_ts(self, ts_dir: str, output_name: str = "output.mp4", delete_source: bool = False):
        """批量合并ts为mp4"""
        list_txt = os.path.join(ts_dir, "file_list.txt")
        ts_files = [f for f in os.listdir(ts_dir) if f.endswith(".ts")]
        ts_files.sort()
        with open(list_txt, "w", encoding="utf-8") as f:
            for ts in ts_files:
                full_path=os.path.join(ts_dir,ts).replace("\\","/")
                f.write(f"file '{full_path}'\n")
        output_mp4 = os.path.join(ts_dir, output_name)
        cmd = [
            self.ffmpeg_path, "-f", "concat", "-safe", "0",
            "-i", list_txt,
            "-c", "copy",
            "-fflags", "+genpts",
            output_mp4
        ]
        subprocess.run(cmd, check=True,cwd=ts_dir)
        os.remove(list_txt)
        print(f"合并完成：{output_mp4}")
        if delete_source:
            for ts in ts_files:
                os.remove(os.path.join(ts_dir, ts))
            print("--- 临时 ts 已清理")

    def convert(self, input_file: str, output_file: str, codec: Optional[str] = None, extra_args: Optional[List[str]] = None):
        """转码任意视频格式"""
        cmd = [self.ffmpeg_path, "-i", input_file]
        if codec:
            cmd += ["-c:v", codec]
        if extra_args:
            cmd += extra_args
        cmd += [output_file]
        subprocess.run(cmd, check=True)
        print(f"转码完成：{output_file}")

    def extract_audio(self, input_file: str, output_file: str, audio_codec: str = "mp3"):
        """提取音频"""
        cmd = [self.ffmpeg_path, "-i", input_file, "-vn", "-acodec", audio_codec, output_file]
        subprocess.run(cmd, check=True)
        print(f"音频提取完成：{output_file}")

    def screenshot(self, input_file: str, output_file: str, time: str = "00:00:01"):
        """视频截图"""
        cmd = [self.ffmpeg_path, "-i", input_file, "-ss", time, "-vframes", "1", output_file]
        subprocess.run(cmd, check=True)
        print(f"截图完成：{output_file}")

    def batch_convert(self, input_dir: str, output_ext: str = "mp4", codec: Optional[str] = None, extra_args: Optional[List[str]] = None):
        """批量转码文件夹下所有视频"""
        files = [f for f in os.listdir(input_dir) if f.lower().endswith((".ts", ".mp4", ".mkv", ".mov"))]
        for f in files:
            input_file = os.path.join(input_dir, f)
            output_file = os.path.splitext(input_file)[0] + "." + output_ext
            self.convert(input_file, output_file, codec, extra_args)

# 示例用法：
if __name__ == "__main__":
    tool = FFmpegTool()
    # 合并ts
    # tool.merge_ts(r"D:/image/video/疯狂动物城", output_name="疯狂动物城.mp4", delete_source=False)
    # 转码
    # tool.convert("input.mkv", "output.mp4", codec="libx264")
    # 提取音频
    # tool.extract_audio("input.mp4", "output.mp3")
    # 截图
    # tool.screenshot("input.mp4", "thumb.jpg", time="00:00:10")
    # 批量转码
    # tool.batch_convert(r"D:/image/video/", output_ext="mp4", codec="libx264")
