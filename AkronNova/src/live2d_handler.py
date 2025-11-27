"""
Live2D Handler for AkronNova Desktop Character
Integrates Live2D functionality with the PyQt desktop application
"""
import json
import chardet
import os
from loguru import logger
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QPainter, QPixmap, QPen, QColor
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
from PyQt6.QtWebChannel import QWebChannel


class Live2DModel:
    """
    A class to represent a Live2D model. This class prepares and stores information about the Live2D model.
    """
    
    def __init__(self, live2d_model_name: str, model_dict_path: str = "../model_dict.json"):
        self.model_dict_path: str = model_dict_path
        self.live2d_model_name: str = live2d_model_name
        self.set_model(live2d_model_name)

    def set_model(self, model_name: str) -> None:
        """
        Set the model with its name and load the model information.
        """
        self.model_info: dict = self._lookup_model_info(model_name)
        self.emo_map: dict = {
            k.lower(): v for k, v in self.model_info["emotionMap"].items()
        }
        self.emo_str: str = " ".join([f"[{key}]," for key in self.emo_map.keys()])
        logger.info("Model Information Loaded.")

    def _load_file_content(self, file_path: str) -> str:
        """Load the content of a file with robust encoding handling."""
        encodings = ["utf-8", "utf-8-sig", "gbk", "gb2312", "ascii"]

        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as file:
                    return file.read()
            except UnicodeDecodeError:
                continue

        try:
            with open(file_path, "rb") as file:
                raw_data = file.read()
            detected = chardet.detect(raw_data)
            detected_encoding = detected["encoding"]

            if detected_encoding:
                try:
                    return raw_data.decode(detected_encoding)
                except UnicodeDecodeError:
                    pass
        except Exception as e:
            logger.error(f"Error detecting encoding for {file_path}: {e}")

        raise UnicodeError(f"Failed to decode {file_path} with any encoding")

    def _lookup_model_info(self, model_name: str) -> dict:
        """
        Find the model information from the model dictionary and return the information about the matched model.
        """
        self.live2d_model_name = model_name

        try:
            file_content = self._load_file_content(self.model_dict_path)
            model_dict = json.loads(file_content)
        except FileNotFoundError as file_e:
            logger.critical(
                f"Model dictionary file not found at {self.model_dict_path}."
            )
            raise file_e
        except json.JSONDecodeError as json_e:
            logger.critical(
                f"Error decoding JSON from model dictionary file at {self.model_dict_path}."
            )
            raise json_e
        except UnicodeError as uni_e:
            logger.critical(
                f"Error reading model dictionary file at {self.model_dict_path}."
            )
            raise uni_e
        except Exception as e:
            logger.critical(
                f"Error occurred while reading model dictionary file at {self.model_dict_path}."
            )
            raise e

        matched_model = next(
            (model for model in model_dict if model["name"] == model_name), None
        )

        if matched_model is None:
            logger.critical(f"Unable to find {model_name} in {self.model_dict_path}.")
            raise KeyError(
                f"{model_name} not found in model dictionary {self.model_dict_path}."
            )

        return matched_model

    def extract_emotion(self, str_to_check: str) -> list:
        """
        Check the input string for any emotion keywords and return a list of values (the expression index) of the emotions found in the string.
        """
        expression_list = []
        str_to_check = str_to_check.lower()

        i = 0
        while i < len(str_to_check):
            if str_to_check[i] != "[":
                i += 1
                continue
            for key in self.emo_map.keys():
                emo_tag = f"[{key}]"
                if str_to_check[i : i + len(emo_tag)] == emo_tag:
                    expression_list.append(self.emo_map[key])
                    i += len(emo_tag) - 1
                    break
            i += 1
        return expression_list

    def remove_emotion_keywords(self, target_str: str) -> str:
        """
        Remove the emotion keywords from the input string and return the cleaned string.
        """
        lower_str = target_str.lower()

        for key in self.emo_map.keys():
            lower_key = f"[{key}]".lower()
            while lower_key in lower_str:
                start_index = lower_str.find(lower_key)
                end_index = start_index + len(lower_key)
                target_str = target_str[:start_index] + target_str[end_index:]
                lower_str = lower_str[:start_index] + lower_str[end_index:]
        return target_str


class Live2DWebView(QWebEngineView):
    """
    A WebView widget to render Live2D models using HTML/JavaScript
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_web_view()
        
    def setup_web_view(self):
        """Setup the web view to display Live2D content"""
        # Load the Live2D HTML page
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(current_dir, "..", "web", "index.html")
        self.load(QUrl.fromLocalFile(html_path))
        
        # Set transparent background
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        # self.setStyleSheet("background:transparent;")
        
        # Enable webgl and other necessary features
        settings = self.settings()
        settings.setAttribute(settings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(settings.WebAttribute.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(settings.WebAttribute.WebGLEnabled, True)
        
    def set_emotion(self, emotion_index: int):
        """Set the emotion for the Live2D model via JavaScript"""
        script = f"window.setLive2DEmotion({emotion_index});"
        self.page().runJavaScript(script)


class Live2DIntegration:
    """
    Integration class that connects Live2D functionality with the AkronNova application
    """
    def __init__(self):
        self.live2d_model = Live2DModel("香風智乃")
        self.current_emotion = 0  # Default neutral emotion
        self.is_loaded = False
        
    def process_text_for_emotions(self, text: str) -> tuple:
        """
        Process text to extract emotions and return clean text
        Returns: (emotion_list, clean_text)
        """
        emotions = self.live2d_model.extract_emotion(text)
        clean_text = self.live2d_model.remove_emotion_keywords(text)
        return emotions, clean_text
    
    def set_emotion(self, emotion_index: int):
        """
        Set the current emotion for the Live2D model
        """
        self.current_emotion = emotion_index
        logger.info(f"Set Live2D emotion to index: {emotion_index}")
        
    def get_available_emotions(self):
        """
        Get available emotions for the current model
        """
        return self.live2d_model.emo_map