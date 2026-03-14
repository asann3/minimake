"""
minimake - シンプルなビルドシステム

このファイルには、ビルドシステムの基本的な機能を実装します。
TODO コメントがある箇所を実装してください。
"""

import json
import subprocess
import sys


def load_build_file(path: str) -> dict:
    """
    ビルド定義ファイル（JSON）を読み込んで辞書として返す

    Args:
        path: ファイルパス（例: "build.json"）

    Returns:
        パースされた辞書
    """
    with open(path, "r") as f:
        return json.load(f)


def build_target(config: dict, target: str) -> bool:
    """
    指定されたターゲットをビルドする

    Args:
        config: load_build_file で読み込んだ設定
        target: ビルドするターゲット名（例: "hello.o"）

    Returns:
        ビルド成功なら True、失敗なら False
    """
    targets = config.get("targets", {})

    # ターゲットが存在するか確認
    if target not in targets:
        print(f"Error: Unknown target '{target}'", file=sys.stderr)
        return False

    target_config = targets[target]
    command = target_config.get("command")

    # コマンドが指定されているか確認
    if not command:
        print(f"Error: No command for target '{target}'", file=sys.stderr)
        return False

    print(f"Building {target}...")
    print(f"  $ {command}")

    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"Error: Build failed for target '{target}'", file=sys.stderr)
        return False
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: minimake <target>... [--file build_file]", file=sys.stderr)
        sys.exit(1)

    target = sys.argv[1]
    build_file = sys.argv[2] if len(sys.argv) > 2 else "build.json"

    config = load_build_file(build_file)

    if not build_target(config, target):
        sys.exit(1)


if __name__ == "__main__":
    main()
