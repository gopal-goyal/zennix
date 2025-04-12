# zennix/core/project_scanner.py

import os
from zennix.utils.logger import get_logger
from zennix.modules.project_metadata import ProjectMetadata, FileInfo, FolderInfo
from typing import List, Dict, Optional, Tuple
from collections import Counter


logger = get_logger("scanner")

class ProjectScanner:
    def __init__(self, project_path: str, deep_scan: bool):
        self.project_path = os.path.abspath(project_path)
        self.deep_scan = deep_scan
        self.ignored_folders = {".git", "__pycache__", "venv", ".venv", "node_modules", "dist", "build", ".idea", ".vscode"}
        logger.info(f"🛰️  Scanner initialized for path: {self.project_path} (deep={self.deep_scan})")

    def scan(self) -> ProjectMetadata:
        logger.info("🔍 Starting project scan...\n")

        folders_info = self._scan_folders()
        files_info = self._scan_files(folders_info)
        languages, primary_lang = self._detect_languages(files_info)
        entry_points = self._find_entry_points(files_info)

        logger.info("✅ Metadata extraction complete")

        return ProjectMetadata(
            root_path=self.project_path,
            folders=folders_info,
            files=files_info,
            languages=languages,
            primary_language=primary_lang,
            entry_points=entry_points,
            # You can fill more metadata fields in future
        )

    def _scan_folders(self) -> List[FolderInfo]:
        logger.info("📁 Scanning folders...")
        folders = []

        for root, dirs, _ in os.walk(self.project_path):
            dirs[:] = [d for d in dirs if d not in self.ignored_folders]
            rel_root = os.path.relpath(root, self.project_path)
            folder_name = "." if rel_root == "." else rel_root
            folder_depth = rel_root.count(os.sep)
            indent = "│   " * folder_depth
            folders.append(FolderInfo(name=folder_name, files=len(os.listdir(root))))
            logger.info(f"{indent}📁 {folder_name}/")

        return folders

    def _scan_files(self, folders_info: List[FolderInfo]) -> List[FileInfo]:
        logger.info("📄 Scanning files...")
        files = []

        for folder in folders_info:
            folder_path = os.path.join(self.project_path, folder.name)
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                if os.path.isfile(file_path):
                    ext = self._get_extension(file)
                    lines = self._count_lines(file_path)
                    relative_path = os.path.relpath(file_path, self.project_path)
                    files.append(FileInfo(path=relative_path, ext=ext, lines=lines))

                    depth = folder.name.count(os.sep)
                    indent = "│   " * depth
                    logger.info(f"{indent}│   └── 📄 {file} ({ext}, {lines} lines)")

        return files

    def _get_extension(self, filename: str) -> str:
        return os.path.splitext(filename)[-1].lower()

    def _count_lines(self, file_path: str) -> int:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return sum(1 for _ in f)
        except Exception:
            return 0

    def _detect_languages(self, files: List[FileInfo]) -> Tuple[Dict[str, int], str]:

        ext_lang_map = {
            ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript", ".java": "Java",
            ".cpp": "C++", ".c": "C", ".cs": "C#", ".go": "Go", ".rb": "Ruby",
        }

        lang_count = Counter()
        for file in files:
            lang = ext_lang_map.get(file.ext)
            if lang:
                lang_count[lang] += 1

        languages = dict(lang_count)
        primary = lang_count.most_common(1)[0][0] if lang_count else ""

        logger.info(f"🧠 Detected languages: {languages}")
        return languages, primary

    def _find_entry_points(self, files: List[FileInfo]) -> List[str]:
        entry_keywords = {"main.py", "index.js", "app.py", "run.py", "cli.py"}
        entry_points = [file.path for file in files if os.path.basename(file.path) in entry_keywords]
        if entry_points:
            logger.info(f"🚀 Entry points: {entry_points}")
        return entry_points

