from __future__ import annotations

import json
import os
import shutil
from typing import Optional
from .utils import resource_path

from PyQt6.QtCore import Qt, QSize, QTimer, pyqtSignal, QThread
from PyQt6.QtGui import (
    QColor,
    QIcon,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
    QMovie,
    QRadialGradient,
)
from PyQt6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFrame,
    QGridLayout,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSlider,
    QSizePolicy,
    QSpinBox,
    QStackedWidget,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

class NoScrollComboBox(QComboBox):
    """QComboBox che ignora la rotellina se non ha il focus."""
    def wheelEvent(self, event):
        if self.hasFocus():
            super().wheelEvent(event)
        else:
            event.ignore()


class NoScrollSpinBox(QSpinBox):
    """QSpinBox che ignora la rotellina se non ha il focus."""
    def wheelEvent(self, event):
        if self.hasFocus():
            super().wheelEvent(event)
        else:
            event.ignore()

from src.character import CharacterManager
from src.config_manager import ConfigManager

class StyleManager:
    """Palette e foglio di stile centralizzati con estetica futuristica Cyber Glass per Aura Layer."""

    # Stile A - Cyber Aura (Indaco / Elettrico)
    COLORS_A = {
        "background": "#070A12",
        "sidebar": "#090D18",
        "surface": "#0F172A",
        "surface_alt": "#131C31",
        "surface_hover": "#1A253F",
        "surface_pressed": "#0B1120",
        "panel": "#0D1424",
        "border": "#1E293B",
        "border_strong": "#6366F1",
        "accent": "#6366F1",
        "accent_hover": "#818CF8",
        "accent_pressed": "#4F46E5",
        "accent_soft": "rgba(99, 102, 241, 0.18)",
        "text": "#F1F5F9",
        "text_muted": "#94A3B8",
        "text_dim": "#64748B",
        "success": "#10B981",
        "success_soft": "rgba(16, 185, 129, 0.18)",
        "danger": "#F43F5E",
        "danger_soft": "rgba(244, 63, 94, 0.18)",
        "cyan": "#06B6D4",
    }

    # Stile B - Deep Abyss (Ciano / Elettrico)
    COLORS_B = {
        "background": "#060A12",
        "sidebar": "#070E1A",
        "surface": "#0C1726",
        "surface_alt": "#101F33",
        "surface_hover": "#172A45",
        "surface_pressed": "#081320",
        "panel": "#0A1322",
        "border": "#16283D",
        "border_strong": "#06B6D4",
        "accent": "#06B6D4",
        "accent_hover": "#22D3EE",
        "accent_pressed": "#0891B2",
        "accent_soft": "rgba(6, 182, 212, 0.18)",
        "text": "#F1F5F9",
        "text_muted": "#94A3B8",
        "text_dim": "#64748B",
        "success": "#10B981",
        "success_soft": "rgba(16, 185, 129, 0.18)",
        "danger": "#F43F5E",
        "danger_soft": "rgba(244, 63, 94, 0.18)",
        "cyan": "#38BDF8",
    }

    # Stile C - Neon Violet (Synthwave Purple)
    COLORS_C = {
        "background": "#090714",
        "sidebar": "#0D0A1C",
        "surface": "#140F2B",
        "surface_alt": "#1B143B",
        "surface_hover": "#261C52",
        "surface_pressed": "#0E0A1E",
        "panel": "#100C24",
        "border": "#281D4A",
        "border_strong": "#A855F7",
        "accent": "#A855F7",
        "accent_hover": "#C084FC",
        "accent_pressed": "#9333EA",
        "accent_soft": "rgba(168, 85, 247, 0.18)",
        "text": "#F1F5F9",
        "text_muted": "#A8A29E",
        "text_dim": "#78716C",
        "success": "#10B981",
        "success_soft": "rgba(16, 185, 129, 0.18)",
        "danger": "#F43F5E",
        "danger_soft": "rgba(244, 63, 94, 0.18)",
        "cyan": "#E879F9",
    }

    COLORS = COLORS_A  # Default

    @classmethod
    def set_style(cls, style: str) -> None:
        """Imposta lo stile corrente (A, B o C)."""
        if style == "B":
            cls.COLORS = cls.COLORS_B
        elif style == "C":
            cls.COLORS = cls.COLORS_C
        else:
            cls.COLORS = cls.COLORS_A

    @classmethod
    def get_current_style(cls) -> str:
        """Restituisce lo stile corrente."""
        if cls.COLORS == cls.COLORS_B:
            return "B"
        elif cls.COLORS == cls.COLORS_C:
            return "C"
        return "A"

    DIRECTION_A = COLORS_A

    @classmethod
    def get_stylesheet(cls, direction: str = "A") -> str:
        return cls.stylesheet()

    @classmethod
    def _get_direction_a_stylesheet(cls) -> str:
        return cls.stylesheet()

    @classmethod
    def stylesheet(cls) -> str:
        c = cls.COLORS
        arrow_down = resource_path("loghi/arrow_down.png").replace("\\", "/")
        arrow_up = resource_path("loghi/arrow_up.png").replace("\\", "/")
        return f"""
QMainWindow {{
background: {c['background']};
}}

QWidget {{
color: {c['text']};
font-family: "Segoe UI Variable", "Segoe UI", "Inter", sans-serif;
font-size: 13px;
}}

QLabel {{
border: none;
background: transparent;
}}

QWidget#appRoot, QWidget#contentRoot, QWidget#libraryPage,
QWidget#settingsPage, QWidget#gridPage {{
background: {c['background']};
}}

QWidget#sidebar {{
background: {c['sidebar']};
border-right: 1px solid rgba(255, 255, 255, 0.08);
}}

QLabel#brandName {{
color: {c['text']};
font-size: 16px;
font-weight: 750;
letter-spacing: 0.5px;
}}

QLabel#brandTagline {{
color: {c['text_dim']};
font-size: 11px;
font-weight: 600;
}}

QPushButton#navButton {{
min-height: 42px;
padding: 0 14px;
background: transparent;
border: 1px solid transparent;
border-radius: 12px;
color: {c['text_muted']};
text-align: left;
font-size: 13px;
font-weight: 650;
}}

QPushButton#navButton:hover {{
color: {c['text']};
background: rgba(255, 255, 255, 0.05);
border-color: rgba(255, 255, 255, 0.1);
}}

QPushButton#navButton[active="true"] {{
color: #FFFFFF;
background: {c['accent_soft']};
border: 1px solid {c['border_strong']};
}}

QFrame#sidebarStatus {{
background: rgba(16, 23, 41, 0.7);
border: 1px solid rgba(255, 255, 255, 0.08);
border-radius: 14px;
}}

QLabel#versionLabel {{
color: {c['text_dim']};
font-size: 10px;
font-family: monospace;
}}

QWidget#topBar {{
background: rgba(11, 16, 29, 0.85);
border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}}

QLabel#pageTitle {{
color: {c['text']};
font-size: 19px;
font-weight: 750;
}}

QLabel#pageSubtitle {{
color: {c['text_muted']};
font-size: 12px;
}}

QLabel#activeCounter {{
min-height: 32px;
padding: 0 14px;
background: {c['success_soft']};
color: #34D399;
border: 1px solid rgba(16, 185, 129, 0.35);
border-radius: 12px;
font-size: 11px;
font-weight: 700;
}}

QTabWidget::pane {{
border: none;
background: {c['background']};
}}

QLabel#sectionTitle {{
color: {c['text']};
font-size: 16px;
font-weight: 750;
}}

QLabel#sectionCaption {{
color: {c['text_dim']};
font-size: 11px;
}}

QPushButton {{
min-height: 38px;
padding: 0 16px;
background: rgba(255, 255, 255, 0.05);
color: {c['text']};
border: 1px solid rgba(255, 255, 255, 0.1);
border-radius: 10px;
font-size: 12px;
font-weight: 650;
}}

QPushButton:hover {{
background: rgba(255, 255, 255, 0.09);
border-color: rgba(255, 255, 255, 0.18);
}}

QPushButton:hover:pressed {{
background: rgba(255, 255, 255, 0.03);
}}

QPushButton:disabled {{
background: rgba(255, 255, 255, 0.02);
color: #64748B;
border-color: rgba(255, 255, 255, 0.04);
}}

QPushButton[class="primary"] {{
background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {c['accent']}, stop:1 {c['accent_hover']});
color: #FFFFFF;
border: 1px solid rgba(255, 255, 255, 0.25);
font-weight: 700;
}}

QPushButton[class="primary"]:hover {{
background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {c['accent_hover']}, stop:1 {c['accent']});
border-color: rgba(255, 255, 255, 0.4);
}}

QPushButton[class="primary"]:hover:pressed {{
background: {c['accent_pressed']};
}}

QPushButton[class="secondary"] {{
background: rgba(255, 255, 255, 0.06);
border: 1px solid rgba(255, 255, 255, 0.12);
}}

QPushButton[class="secondary"]:hover {{
background: rgba(255, 255, 255, 0.11);
border-color: {c['border_strong']};
}}

QPushButton[class="danger"] {{
background: {c['danger_soft']};
color: #FB7185;
border: 1px solid rgba(244, 63, 94, 0.3);
}}

QPushButton[class="danger"]:hover {{
background: rgba(244, 63, 94, 0.28);
border-color: rgba(244, 63, 94, 0.5);
}}

QLineEdit, QComboBox, QSpinBox {{
min-height: 38px;
background: rgba(11, 16, 29, 0.85);
color: #FFFFFF;
border: 1px solid rgba(255, 255, 255, 0.1);
border-radius: 10px;
padding: 0 12px;
selection-background-color: {c['accent']};
selection-color: #FFFFFF;
font-size: 12px;
}}

QLineEdit:hover, QComboBox:hover, QSpinBox:hover {{
border-color: rgba(255, 255, 255, 0.22);
}}

QLineEdit:focus, QComboBox:focus, QSpinBox:focus {{
border: 1px solid {c['accent']};
background: rgba(15, 23, 42, 0.95);
}}

QLineEdit::placeholder {{
color: {c['text_dim']};
}}

QComboBox {{
padding-right: 32px;
}}

QComboBox::drop-down {{
subcontrol-origin: padding;
subcontrol-position: top right;
width: 28px;
border: none;
background: transparent;
}}

QComboBox::down-arrow {{
image: url("{arrow_down}");
width: 12px;
height: 12px;
}}

QComboBox QAbstractItemView {{
background: #0F172A;
color: #FFFFFF;
border: 1px solid rgba(255, 255, 255, 0.15);
border-radius: 8px;
outline: 0;
padding: 4px;
selection-background-color: {c['accent']};
selection-color: #FFFFFF;
}}

QSpinBox {{
padding-right: 28px;
}}

QSpinBox::up-button {{
subcontrol-origin: border;
subcontrol-position: top right;
width: 24px;
height: 18px;
border: none;
background: rgba(255, 255, 255, 0.05);
border-top-right-radius: 8px;
}}

QSpinBox::up-button:hover {{
background: rgba(255, 255, 255, 0.18);
}}

QSpinBox::up-arrow {{
image: url("{arrow_up}");
width: 10px;
height: 10px;
}}

QSpinBox::down-button {{
subcontrol-origin: border;
subcontrol-position: bottom right;
width: 24px;
height: 18px;
border: none;
background: rgba(255, 255, 255, 0.05);
border-bottom-right-radius: 8px;
}}

QSpinBox::down-button:hover {{
background: rgba(255, 255, 255, 0.18);
}}

QSpinBox::down-arrow {{
image: url("{arrow_down}");
width: 10px;
height: 10px;
}}

QSlider::groove:horizontal {{
height: 4px;
background: rgba(255, 255, 255, 0.15);
border-radius: 2px;
}}

QSlider::sub-page:horizontal {{
background: {c['accent']};
border-radius: 2px;
}}

QSlider::handle:horizontal {{
background: #FFFFFF;
border: 2px solid {c['accent']};
width: 14px;
margin-top: -5px;
margin-bottom: -5px;
border-radius: 7px;
}}

QSlider::handle:horizontal:hover {{
background: #FFFFFF;
border-color: {c['accent_hover']};
}}

QScrollArea {{
border: none;
background: transparent;
}}

QScrollArea > QWidget > QWidget {{
background: transparent;
}}

QScrollBar:vertical {{
width: 7px;
margin: 2px 0;
background: transparent;
}}

QScrollBar::handle:vertical {{
min-height: 26px;
background: rgba(255, 255, 255, 0.15);
border-radius: 3px;
}}

QScrollBar::handle:vertical:hover {{
background: rgba(255, 255, 255, 0.3);
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
height: 0;
width: 0;
}}

QFrame#librarySurface, QFrame#detailsPanel, QFrame#settingsCard {{
background: rgba(13, 20, 36, 0.7);
border: 1px solid rgba(255, 255, 255, 0.08);
border-radius: 18px;
}}

QFrame#characterCard {{
background: rgba(15, 23, 42, 0.65);
border: 1px solid rgba(255, 255, 255, 0.08);
border-radius: 14px;
}}

QFrame#characterCard:hover {{
background: rgba(22, 33, 58, 0.8);
border: 1px solid {c['border_strong']};
}}

QFrame#characterCard[selected="true"] {{
background: rgba(28, 38, 70, 0.9);
border: 2px solid {c['accent']};
}}

QFrame#characterCard[selected="true"] QLabel#cardName {{
color: #FFFFFF;
}}

QLabel#cardName {{
color: {c['text']};
font-size: 13px;
font-weight: 700;
}}

QLabel#cardStatus {{
color: {c['text_dim']};
font-size: 11px;
font-weight: 600;
}}

QLabel#cardStatus[active="true"] {{
color: #34D399;
}}

QLabel#audioPathLabel {{
color: {c['text_muted']};
font-size: 11px;
font-style: italic;
}}

QCheckBox#settingsCheckbox {{
color: {c['text']};
font-size: 12px;
spacing: 6px;
}}

QCheckBox#settingsCheckbox::indicator {{
width: 16px;
height: 16px;
border: 1px solid rgba(255, 255, 255, 0.2);
border-radius: 4px;
background: rgba(11, 16, 29, 0.8);
}}

QCheckBox#settingsCheckbox::indicator:checked {{
background: {c['accent']};
border-color: {c['accent']};
}}

QCheckBox#settingsCheckbox::indicator:hover {{
border-color: {c['accent']};
}}

QLabel#hotkeyDisplay {{
color: {c['accent']};
font-size: 12px;
font-weight: 600;
padding: 4px 8px;
background: rgba(15, 23, 42, 0.8);
border: 1px solid rgba(255, 255, 255, 0.1);
border-radius: 6px;
font-family: monospace;
}}

QLabel#folderPath {{
color: {c['text_muted']};
font-size: 11px;
font-family: monospace;
}}

QLabel#infoText {{
color: {c['text_dim']};
font-size: 11px;
padding: 2px 0;
}}

QLabel#panelEyebrow, QLabel#fieldLabel {{
color: {c['text_muted']};
font-size: 11px;
font-weight: 750;
letter-spacing: 0.8px;
border: none;
background: transparent;
}}

QLabel#fieldHint {{
color: {c['text_dim']};
font-size: 10px;
font-family: monospace;
border: none;
background: transparent;
}}

QLabel#characterName {{
color: {c['text']};
font-size: 18px;
font-weight: 780;
}}

QLabel#statusBadge {{
min-height: 24px;
padding: 0 10px;
background: rgba(255, 255, 255, 0.06);
color: {c['text_muted']};
border: 1px solid rgba(255, 255, 255, 0.1);
border-radius: 12px;
font-size: 10px;
font-weight: 700;
font-family: monospace;
}}

QLabel#statusBadge[status="active"] {{
background: {c['success_soft']};
color: #34D399;
border-color: rgba(16, 185, 129, 0.35);
}}

QLabel#statusBadge[status="inactive"] {{
background: rgba(255, 255, 255, 0.05);
color: {c['text_dim']};
border-color: rgba(255, 255, 255, 0.1);
}}

QFrame#divider {{
min-height: 1px;
max-height: 1px;
background: rgba(255, 255, 255, 0.08);
border: none;
}}

QLabel#emptyTitle {{
color: {c['text']};
font-size: 16px;
font-weight: 750;
}}

QLabel#emptyText {{
color: {c['text_muted']};
font-size: 12px;
}}

QLabel#comingSoonBadge {{
min-height: 22px;
padding: 0 8px;
background: {c['accent_soft']};
color: {c['accent']};
border: 1px solid {c['border_strong']};
border-radius: 10px;
font-size: 10px;
font-weight: 750;
}}

QToolTip {{
background: #0F172A;
color: #FFFFFF;
border: 1px solid rgba(255, 255, 255, 0.15);
padding: 6px 10px;
border-radius: 6px;
}}

QMessageBox, QInputDialog {{
background: #0D1424;
}}
"""


def repolish(widget: QWidget) -> None:
    """Aggiorna il QSS dopo la modifica di una proprietà dinamica."""
    widget.style().unpolish(widget)
    widget.style().polish(widget)
    widget.update()


def add_shadow(
    widget: QWidget,
    blur: int = 28,
    y_offset: int = 8,
    alpha: int = 90,
    color: Optional[QColor] = None,
) -> None:
    shadow = QGraphicsDropShadowEffect(widget)
    shadow.setBlurRadius(blur)
    shadow.setOffset(0, y_offset)
    shadow_color = QColor(color) if color is not None else QColor(0, 0, 0)
    shadow_color.setAlpha(alpha)
    shadow.setColor(shadow_color)
    widget.setGraphicsEffect(shadow)


def make_icon(name: str, color: str = "#DCE4F0", size: int = 20) -> QIcon:
    """Crea piccole icone vettoriali senza dipendenze o font esterni."""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    pen = QPen(QColor(color))
    pen.setWidthF(max(1.5, size * 0.085))
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    painter.setPen(pen)
    painter.setBrush(Qt.BrushStyle.NoBrush)

    s = float(size)

    if name == "library":
        cell = s * 0.27
        gap = s * 0.13
        start = s * 0.17
        for row in range(2):
            for col in range(2):
                x = start + col * (cell + gap)
                y = start + row * (cell + gap)
                painter.drawRoundedRect(int(x), int(y), int(cell), int(cell), 2, 2)

    elif name == "settings":
        ys = (s * 0.27, s * 0.50, s * 0.73)
        knobs = (s * 0.38, s * 0.66, s * 0.45)
        for y, knob_x in zip(ys, knobs):
            painter.drawLine(int(s * 0.16), int(y), int(s * 0.84), int(y))
            painter.setBrush(QColor(color))
            painter.drawEllipse(
                int(knob_x - s * 0.07), int(y - s * 0.07), int(s * 0.14), int(s * 0.14)
            )
            painter.setBrush(Qt.BrushStyle.NoBrush)

    elif name == "search":
        painter.drawEllipse(int(s * 0.18), int(s * 0.16), int(s * 0.48), int(s * 0.48))
        painter.drawLine(int(s * 0.59), int(s * 0.59), int(s * 0.82), int(s * 0.82))

    elif name == "add":
        painter.drawLine(int(s * 0.50), int(s * 0.22), int(s * 0.50), int(s * 0.78))
        painter.drawLine(int(s * 0.22), int(s * 0.50), int(s * 0.78), int(s * 0.50))

    elif name == "play":
        path = QPainterPath()
        path.moveTo(s * 0.34, s * 0.23)
        path.lineTo(s * 0.78, s * 0.50)
        path.lineTo(s * 0.34, s * 0.77)
        path.closeSubpath()
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(color))
        painter.drawPath(path)

    elif name == "stop":
        painter.setBrush(QColor(color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(
            int(s * 0.28), int(s * 0.28), int(s * 0.44), int(s * 0.44), 3, 3
        )

    elif name == "edit":
        painter.drawLine(int(s * 0.25), int(s * 0.72), int(s * 0.67), int(s * 0.30))
        painter.drawLine(int(s * 0.58), int(s * 0.25), int(s * 0.74), int(s * 0.41))
        painter.drawLine(int(s * 0.23), int(s * 0.75), int(s * 0.39), int(s * 0.71))

    elif name == "trash":
        painter.drawRoundedRect(
            int(s * 0.28), int(s * 0.31), int(s * 0.44), int(s * 0.49), 2, 2
        )
        painter.drawLine(int(s * 0.23), int(s * 0.27), int(s * 0.77), int(s * 0.27))
        painter.drawLine(int(s * 0.41), int(s * 0.18), int(s * 0.59), int(s * 0.18))
        painter.drawLine(int(s * 0.43), int(s * 0.42), int(s * 0.43), int(s * 0.68))
        painter.drawLine(int(s * 0.57), int(s * 0.42), int(s * 0.57), int(s * 0.68))

    elif name == "image":
        painter.drawRoundedRect(
            int(s * 0.16), int(s * 0.18), int(s * 0.68), int(s * 0.64), 4, 4
        )
        painter.drawEllipse(int(s * 0.57), int(s * 0.29), int(s * 0.12), int(s * 0.12))
        path = QPainterPath()
        path.moveTo(s * 0.23, s * 0.70)
        path.lineTo(s * 0.42, s * 0.48)
        path.lineTo(s * 0.54, s * 0.61)
        path.lineTo(s * 0.65, s * 0.50)
        path.lineTo(s * 0.78, s * 0.70)
        painter.drawPath(path)

    painter.end()
    return QIcon(pixmap)


def draw_brand_mark(size: int = 42) -> QPixmap:
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    gradient = QLinearGradient(0, 0, size, size)
    gradient.setColorAt(0, QColor("#6366F1"))
    gradient.setColorAt(1, QColor("#06B6D4"))
    painter.setBrush(gradient)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawRoundedRect(
        0, 0, size, size, int(size * 0.28), int(size * 0.28)
    )

    painter.setBrush(Qt.BrushStyle.NoBrush)
    pen = QPen(QColor("#FFFFFF"))
    pen.setWidthF(max(2.0, size * 0.075))
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    painter.setPen(pen)
    painter.drawEllipse(
        int(size * 0.22), int(size * 0.30), int(size * 0.56), int(size * 0.37)
    )
    painter.drawEllipse(
        int(size * 0.31), int(size * 0.21), int(size * 0.38), int(size * 0.56)
    )

    painter.setBrush(QColor("#FFFFFF"))
    painter.setPen(Qt.PenStyle.NoPen)
    dot = max(3, int(size * 0.12))
    painter.drawEllipse((size - dot) // 2, (size - dot) // 2, dot, dot)
    painter.end()
    return pixmap


def draw_placeholder_icon(size_w: int, size_h: int, glyph_scale: float = 0.34) -> QPixmap:
    """Anteprima vettoriale usata quando il file immagine non è caricabile."""
    pixmap = QPixmap(size_w, size_h)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    gradient = QLinearGradient(0, 0, size_w, size_h)
    gradient.setColorAt(0, QColor("#0D1424"))
    gradient.setColorAt(1, QColor("#162035"))
    painter.setBrush(gradient)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawRoundedRect(0, 0, size_w, size_h, 16, 16)

    glow = QRadialGradient(size_w * 0.76, size_h * 0.15, max(size_w, size_h) * 0.58)
    glow.setColorAt(0, QColor(99, 102, 241, 50))
    glow.setColorAt(1, QColor(99, 102, 241, 0))
    painter.setBrush(glow)
    painter.drawRoundedRect(0, 0, size_w, size_h, 16, 16)

    glyph_w = min(size_w, size_h) * glyph_scale
    cx, cy = size_w / 2, size_h / 2

    pen = QPen(QColor("#8592A6"))
    pen.setWidthF(max(1.7, glyph_w * 0.055))
    pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    painter.setPen(pen)
    painter.setBrush(Qt.BrushStyle.NoBrush)

    frame_w = glyph_w * 1.55
    frame_h = glyph_w * 1.12
    frame_x = cx - frame_w / 2
    frame_y = cy - frame_h / 2
    painter.drawRoundedRect(int(frame_x), int(frame_y), int(frame_w), int(frame_h), 8, 8)

    path = QPainterPath()
    path.moveTo(frame_x + frame_w * 0.12, frame_y + frame_h * 0.78)
    path.lineTo(frame_x + frame_w * 0.38, frame_y + frame_h * 0.48)
    path.lineTo(frame_x + frame_w * 0.55, frame_y + frame_h * 0.66)
    path.lineTo(frame_x + frame_w * 0.70, frame_y + frame_h * 0.50)
    path.lineTo(frame_x + frame_w * 0.88, frame_y + frame_h * 0.78)
    painter.drawPath(path)

    sun_r = max(3, int(glyph_w * 0.10))
    painter.drawEllipse(
        int(frame_x + frame_w * 0.67),
        int(frame_y + frame_h * 0.20),
        sun_r * 2,
        sun_r * 2,
    )

    painter.end()
    return pixmap


def load_thumbnail(
    source_path: str,
    width: int,
    height: Optional[int] = None,
    radius: int = 14,
) -> Optional[QPixmap]:
    """Carica e ritaglia un'immagine nel formato richiesto, con angoli arrotondati."""
    if height is None:
        height = width

    if not source_path or not os.path.exists(source_path):
        return None

    raw = QPixmap(source_path)
    if raw.isNull():
        return None

    scaled = raw.scaled(
        width,
        height,
        Qt.AspectRatioMode.KeepAspectRatioByExpanding,
        Qt.TransformationMode.SmoothTransformation,
    )

    x = max(0, (scaled.width() - width) // 2)
    y = max(0, (scaled.height() - height) // 2)
    cropped = scaled.copy(x, y, width, height)

    rounded = QPixmap(width, height)
    rounded.fill(Qt.GlobalColor.transparent)
    painter = QPainter(rounded)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    path = QPainterPath()
    path.addRoundedRect(0, 0, width, height, radius, radius)
    painter.setClipPath(path)
    painter.drawPixmap(0, 0, cropped)
    painter.end()
    return rounded


class AuraArtwork(QWidget):
    """Elemento decorativo legacy (rimosso in v2.5)."""
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.hide()


class CharacterCard(QFrame):
    """Card selezionabile della libreria con stile futuristico Cyber Glass."""

    clicked = pyqtSignal(str)

    # Dimensioni predefinite per ogni taglia
    CARD_SIZES = {
        "small": (140, 180),
        "medium": (174, 222),
        "large": (210, 270)
    }

    def __init__(
        self,
        character_name: str,
        character_path: str,
        animation_path: str,
        parent: Optional[QWidget] = None,
        active: bool = False,
        grid_size: str = "medium",
        translations=None,
    ):
        super().__init__(parent)
        self.character_name = character_name
        self.character_path = character_path
        self.animation_path = animation_path
        self.is_selected = False
        self.is_active = active
        self.movie: Optional[QMovie] = None
        self.thumbnail_pixmap: Optional[QPixmap] = None
        self.grid_size = grid_size
        self.translations = translations
        self.setup_ui()

    def setup_ui(self) -> None:
        self.setObjectName("characterCard")
        self.setProperty("selected", "false")

        # Usa dimensioni basate sulla taglia
        card_width, card_height = self.CARD_SIZES.get(self.grid_size, self.CARD_SIZES["medium"])
        self.setFixedSize(card_width, card_height)

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(11, 11, 11, 12)
        layout.setSpacing(8)

        # Dimensione preview proporzionale alla card
        preview_size = int(card_width * 0.86)
        self.preview = QLabel()
        self.preview.setFixedSize(preview_size, preview_size)
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview.setStyleSheet("background: rgba(8, 12, 22, 0.7); border: 1px solid rgba(255, 255, 255, 0.07); border-radius: 10px;")
        self.preview.setScaledContents(True)

        # Genera e imposta thumbnail statico come anteprima predefinita a basso consumo
        thumbnail = load_thumbnail(self.animation_path, preview_size, preview_size, 10)
        self.thumbnail_pixmap = (
            thumbnail
            if thumbnail is not None
            else draw_placeholder_icon(preview_size, preview_size, 0.29)
        )
        self.preview.setPixmap(self.thumbnail_pixmap)

        # Inizializza QMovie solo se è una GIF (senza avviare il loop per risparmiare CPU)
        if self.animation_path.lower().endswith(".gif"):
            self.movie = QMovie(self.animation_path)
            if self.movie.isValid():
                self.movie.setScaledSize(QSize(preview_size, preview_size))
            else:
                self.movie = None

        layout.addWidget(self.preview, 0, Qt.AlignmentFlag.AlignCenter)

        self.name_label = QLabel(self.character_name)
        self.name_label.setObjectName("cardName")
        self.name_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        self.name_label.setToolTip(self.character_name)
        self.name_label.setMaximumHeight(20)
        layout.addWidget(self.name_label)

        status_row = QHBoxLayout()
        status_row.setContentsMargins(0, 0, 0, 0)
        status_row.setSpacing(6)

        self.status_dot = QLabel()
        self.status_dot.setFixedSize(7, 7)
        status_row.addWidget(self.status_dot)

        self.status_label = QLabel()
        self.status_label.setObjectName("cardStatus")
        status_row.addWidget(self.status_label)
        status_row.addStretch()
        layout.addLayout(status_row)

        self.set_active(self.is_active)

    def enterEvent(self, event) -> None:
        """Avvia l'animazione GIF solo al passaggio del mouse per ottimizzare la CPU."""
        super().enterEvent(event)
        if self.movie and self.movie.isValid():
            self.preview.setMovie(self.movie)
            if self.movie.state() != QMovie.MovieState.Running:
                self.movie.start()

    def leaveEvent(self, event) -> None:
        """Ferma l'animazione GIF quando il mouse esce, salvo che la card sia selezionata."""
        super().leaveEvent(event)
        if not self.is_selected and self.movie:
            if self.movie.state() == QMovie.MovieState.Running:
                self.movie.stop()
            self.preview.setMovie(None)
            if self.thumbnail_pixmap:
                self.preview.setPixmap(self.thumbnail_pixmap)

    def set_selected(self, selected: bool) -> None:
        self.is_selected = selected
        self.setProperty("selected", "true" if selected else "false")
        repolish(self)

        if selected:
            glow = QColor(StyleManager.COLORS["accent"])
            add_shadow(self, blur=24, y_offset=2, alpha=70, color=glow)
            # Se la card è selezionata, avvia il preview animato
            if self.movie and self.movie.isValid():
                self.preview.setMovie(self.movie)
                if self.movie.state() != QMovie.MovieState.Running:
                    self.movie.start()
        else:
            self.setGraphicsEffect(None)
            # Se la card non è più selezionata e il mouse non è sopra, ferma il movie
            if not self.underMouse() and self.movie:
                if self.movie.state() == QMovie.MovieState.Running:
                    self.movie.stop()
                self.preview.setMovie(None)
                if self.thumbnail_pixmap:
                    self.preview.setPixmap(self.thumbnail_pixmap)

    def set_active(self, active: bool) -> None:
        self.is_active = active
        self.status_label.setProperty("active", "true" if active else "false")
        status_active_text = self.translations.get("status_active_desktop", "Attivo sul desktop") if self.translations else "Attivo sul desktop"
        status_ready_text = self.translations.get("status_ready", "Pronto") if self.translations else "Pronto"
        self.status_label.setText(status_active_text if active else status_ready_text)
        self.status_dot.setStyleSheet(
            "background: #10B981; border-radius: 3px;"
            if active
            else "background: rgba(255, 255, 255, 0.2); border-radius: 3px;"
        )
        repolish(self.status_label)
        repolish(self.status_label)

    def cleanup_movie(self) -> None:
        """Ferma e pulisce il movie per evitare memory leak."""
        if self.movie:
            self.movie.stop()
            self.preview.setMovie(None)
            self.movie = None

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.character_name)
        super().mousePressEvent(event)


class LauncherWindow(QMainWindow):
    """Finestra principale del launcher Aura Layer."""

    character_selected = pyqtSignal(str)
    character_launched = pyqtSignal(str)
    character_deactivated = pyqtSignal(str)
    character_removed = pyqtSignal(str)
    character_renamed = pyqtSignal(str, str)
    character_updated = pyqtSignal(str)
    character_lock_changed = pyqtSignal(str, bool)  # character_name, locked
    global_fps_changed = pyqtSignal(int)
    quit_requested = pyqtSignal()  # Richiesta di chiusura dell'app

    def __init__(
        self, character_manager: CharacterManager, config_manager=None, translations=None, parent: Optional[QWidget] = None
    ):
        super().__init__(parent)
        self.character_manager = character_manager
        self.config_manager = config_manager
        self.translations = translations
        self.selected_character: Optional[str] = None
        self.active_characters: set[str] = set()
        self.character_cards: dict[str, CharacterCard] = {}
        self.current_filter = ""
        self.current_sort = "az"
        self.details_movie: Optional[QMovie] = None

        self.setup_ui()
        if self.config_manager:
            self.initialize_style_selector()
            self.initialize_settings()
        self.load_characters()

    # ------------------------------------------------------------------ UI
    def setup_ui(self) -> None:
        self.setWindowTitle("Aura Layer")
        self.setMinimumSize(1120, 720)
        self.resize(1320, 830)
        self.setStyleSheet(StyleManager.stylesheet())

        logo_path = resource_path("loghi/logo_mini.png")
        if os.path.exists(logo_path):
            self.setWindowIcon(QIcon(logo_path))

        root = QWidget()
        root.setObjectName("appRoot")
        self.setCentralWidget(root)

        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.sidebar = self._create_sidebar()
        root_layout.addWidget(self.sidebar)

        content_root = QWidget()
        content_root.setObjectName("contentRoot")
        content_layout = QVBoxLayout(content_root)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        root_layout.addWidget(content_root, 1)

        self.top_bar = self._create_top_bar()
        content_layout.addWidget(self.top_bar)

        self.tab_widget = QTabWidget()
        self.tab_widget.setDocumentMode(True)
        self.tab_widget.tabBar().hide()
        content_layout.addWidget(self.tab_widget, 1)

        self.library_tab = self.create_library_tab()
        self.settings_tab = self.create_settings_tab()
        tab_library_text = self.translations.get("tab_library", "Libreria") if self.translations else "Libreria"
        tab_settings_text = self.translations.get("tab_settings", "Impostazioni") if self.translations else "Impostazioni"
        self.tab_widget.addTab(self.library_tab, tab_library_text)
        self.tab_widget.addTab(self.settings_tab, tab_settings_text)

        self.nav_library.clicked.connect(lambda: self.set_page(0))
        self.nav_settings.clicked.connect(lambda: self.set_page(1))
        self.set_page(0)

    def _create_sidebar(self) -> QWidget:
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(224)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(18, 22, 18, 18)
        layout.setSpacing(8)

        brand_row = QHBoxLayout()
        brand_row.setSpacing(11)

        logo = QLabel()
        logo.setFixedSize(42, 42)
        logo_path = resource_path("loghi/logo_mini.png")
        if os.path.exists(logo_path):
            logo_pixmap = QPixmap(logo_path)
            if not logo_pixmap.isNull():
                logo.setPixmap(
                    logo_pixmap.scaled(
                        42,
                        42,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation,
                    )
                )
            else:
                logo.setPixmap(draw_brand_mark(42))
        else:
            logo.setPixmap(draw_brand_mark(42))
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        brand_row.addWidget(logo)

        brand_text = QVBoxLayout()
        brand_text.setSpacing(1)
        brand_name_text = self.translations.get("brand_name", "Aura Layer") if self.translations else "Aura Layer"
        brand_name = QLabel(brand_name_text)
        brand_name.setObjectName("brandName")
        brand_tagline_text = self.translations.get("brand_tagline", "FEDERA PROJECT") if self.translations else "FEDERA PROJECT"
        brand_tagline = QLabel(brand_tagline_text)
        brand_tagline.setObjectName("brandTagline")
        brand_text.addWidget(brand_name)
        brand_text.addWidget(brand_tagline)
        brand_row.addLayout(brand_text)
        brand_row.addStretch()
        layout.addLayout(brand_row)

        layout.addSpacing(20)

        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)

        nav_library_text = self.translations.get("nav_library", "Libreria") if self.translations else "Libreria"
        self.nav_library = self._create_nav_button(nav_library_text, "library")
        nav_settings_text = self.translations.get("tab_settings", "Impostazioni") if self.translations else "Impostazioni"
        self.nav_settings = self._create_nav_button(nav_settings_text, "settings")
        self.nav_group.addButton(self.nav_library, 0)
        self.nav_group.addButton(self.nav_settings, 1)
        layout.addWidget(self.nav_library)
        layout.addWidget(self.nav_settings)
        layout.addStretch()

        # Dummy labels per compatibilità contatori interni
        self.total_stat_value = QLabel("0")
        self.total_stat_value.hide()
        self.active_stat_value = QLabel("0")
        self.active_stat_value.hide()

        status_card = QFrame()
        status_card.setObjectName("sidebarStatus")
        status_layout = QVBoxLayout(status_card)
        status_layout.setContentsMargins(14, 12, 14, 12)
        status_layout.setSpacing(6)

        status_top = QHBoxLayout()
        status_top.setSpacing(7)
        status_dot = QLabel()
        status_dot.setFixedSize(8, 8)
        status_dot.setStyleSheet("background: #10B981; border-radius: 4px;")
        status_top.addWidget(status_dot)
        status_text_text = self.translations.get("status_operational", "Aura Core Attivo") if self.translations else "Aura Core Attivo"
        status_text = QLabel(status_text_text)
        status_text.setStyleSheet("color: #F1F5F9; font-size: 11px; font-weight: 700;")
        status_top.addWidget(status_text)
        status_top.addStretch()
        status_layout.addLayout(status_top)

        self.sidebar_active_stat = QLabel("0 personaggi attivi")
        self.sidebar_active_stat.setStyleSheet("color: #94A3B8; font-size: 11px;")
        status_layout.addWidget(self.sidebar_active_stat)

        version_text = self.translations.get("status_version", "AURA LAYER • FEDERA PROJECT") if self.translations else "AURA LAYER • FEDERA PROJECT"
        version = QLabel(version_text)
        version.setObjectName("versionLabel")
        status_layout.addWidget(version)
        layout.addWidget(status_card)

        return sidebar

    def _create_nav_button(self, text: str, icon_name: str) -> QPushButton:
        button = QPushButton(text)
        button.setObjectName("navButton")
        button.setCheckable(True)
        button.setProperty("active", "false")
        button.setIcon(make_icon(icon_name, "#9AA7BA", 18))
        button.setIconSize(QSize(18, 18))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        return button

    def _create_top_bar(self) -> QWidget:
        top_bar = QWidget()
        top_bar.setObjectName("topBar")
        top_bar.setFixedHeight(68)

        layout = QHBoxLayout(top_bar)
        layout.setContentsMargins(28, 12, 28, 12)
        layout.setSpacing(14)

        titles = QVBoxLayout()
        titles.setSpacing(1)
        page_title_text = self.translations.get("page_library_title", "Libreria") if self.translations else "Libreria"
        self.page_title = QLabel(page_title_text)
        self.page_title.setObjectName("pageTitle")
        page_subtitle_text = self.translations.get("page_library_subtitle", "Gestisci e avvia i personaggi del tuo desktop") if self.translations else "Gestisci e avvia i personaggi del tuo desktop"
        self.page_subtitle = QLabel(page_subtitle_text)
        self.page_subtitle.setObjectName("pageSubtitle")
        titles.addWidget(self.page_title)
        titles.addWidget(self.page_subtitle)
        layout.addLayout(titles)
        layout.addStretch()

        # Barra di ricerca
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Cerca un personaggio...")
        self.search_bar.setClearButtonEnabled(True)
        self.search_bar.setMinimumWidth(220)
        self.search_bar.setMaximumWidth(320)
        self.search_bar.addAction(
            make_icon("search", StyleManager.COLORS["text_dim"], 17),
            QLineEdit.ActionPosition.LeadingPosition,
        )
        self.search_bar.textChanged.connect(self.filter_characters)
        layout.addWidget(self.search_bar)

        # Pulsante Aggiungi da PC
        add_pc_text = self.translations.get("btn_add_pc", "Aggiungi da PC") if self.translations else "Aggiungi da PC"
        self.add_button = QPushButton(add_pc_text)
        self.add_button.setProperty("class", "primary")
        self.add_button.setIcon(make_icon("add", "#FFFFFF", 16))
        self.add_button.setIconSize(QSize(16, 16))
        self.add_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_button.clicked.connect(self.add_character_from_pc)
        layout.addWidget(self.add_button)

        active_counter_text = self.translations.get("active_counter", "0 personaggi attivi") if self.translations else "0 personaggi attivi"
        self.active_counter = QLabel(active_counter_text)
        self.active_counter.setObjectName("activeCounter")
        layout.addWidget(self.active_counter)
        return top_bar

    def set_page(self, index: int) -> None:
        self.tab_widget.setCurrentIndex(index)
        is_library = index == 0

        self.nav_library.setChecked(is_library)
        self.nav_settings.setChecked(not is_library)
        self.nav_library.setProperty("active", "true" if is_library else "false")
        self.nav_settings.setProperty("active", "false" if is_library else "true")
        repolish(self.nav_library)
        repolish(self.nav_settings)

        self.search_bar.setVisible(is_library)
        self.add_button.setVisible(is_library)
        self.active_counter.setVisible(is_library)

        if is_library:
            page_library_title = self.translations.get("page_library_title", "Libreria") if self.translations else "Libreria"
            page_library_subtitle = self.translations.get("page_library_subtitle", "Gestisci e avvia i personaggi del tuo desktop") if self.translations else "Gestisci e avvia i personaggi del tuo desktop"
            self.page_title.setText(page_library_title)
            self.page_subtitle.setText(page_library_subtitle)
        else:
            page_settings_title = self.translations.get("page_settings_title", "Impostazioni") if self.translations else "Impostazioni"
            page_settings_subtitle = self.translations.get("page_settings_subtitle", "Personalizza il comportamento di Aura Layer") if self.translations else "Personalizza il comportamento di Aura Layer"
            self.page_title.setText(page_settings_title)
            self.page_subtitle.setText(page_settings_subtitle)

    def create_library_tab(self) -> QWidget:
        page = QWidget()
        page.setObjectName("libraryPage")

        layout = QVBoxLayout(page)
        layout.setContentsMargins(28, 16, 28, 20)
        layout.setSpacing(12)

        toolbar = QHBoxLayout()
        toolbar.setSpacing(12)

        section_titles = QVBoxLayout()
        section_titles.setSpacing(2)
        library_title_text = self.translations.get("library_title", "I tuoi personaggi") if self.translations else "I tuoi personaggi"
        library_title = QLabel(library_title_text)
        library_title.setObjectName("sectionTitle")
        library_count_text = self.translations.get("library_count", "0 elementi") if self.translations else "0 elementi"
        self.library_count_label = QLabel(library_count_text)
        self.library_count_label.setObjectName("sectionCaption")
        section_titles.addWidget(library_title)
        section_titles.addWidget(self.library_count_label)
        toolbar.addLayout(section_titles)
        toolbar.addStretch()

        self.sort_combo = NoScrollComboBox()
        self.sort_combo.setMinimumWidth(140)
        self.sort_combo.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        sort_az_text = self.translations.get("sort_az", "Nome: A–Z") if self.translations else "Nome: A–Z"
        sort_za_text = self.translations.get("sort_za", "Nome: Z–A") if self.translations else "Nome: Z–A"
        self.sort_combo.addItem(sort_az_text, "az")
        self.sort_combo.addItem(sort_za_text, "za")
        self.sort_combo.currentIndexChanged.connect(self._on_sort_changed)
        toolbar.addWidget(self.sort_combo)
        layout.addLayout(toolbar)

        split_layout = QHBoxLayout()
        split_layout.setSpacing(18)

        library_surface = QFrame()
        library_surface.setObjectName("librarySurface")
        library_surface_layout = QVBoxLayout(library_surface)
        library_surface_layout.setContentsMargins(16, 16, 10, 12)
        library_surface_layout.setSpacing(0)

        self.grid_stack = QStackedWidget()
        self.grid_stack.setStyleSheet("background: transparent; border: none;")
        library_surface_layout.addWidget(self.grid_stack)

        grid_page = QWidget()
        grid_page.setObjectName("gridPage")
        grid_page_layout = QVBoxLayout(grid_page)
        grid_page_layout.setContentsMargins(0, 0, 0, 0)
        grid_page_layout.setSpacing(0)

        self.grid_scroll = QScrollArea()
        self.grid_scroll.setWidgetResizable(True)
        self.grid_scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.grid_scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        self.grid_widget = QWidget()
        self.grid_widget.setStyleSheet("background: transparent;")
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setContentsMargins(0, 0, 6, 0)
        self.grid_layout.setHorizontalSpacing(14)
        self.grid_layout.setVerticalSpacing(14)
        self.grid_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )

        self.grid_scroll.setWidget(self.grid_widget)
        grid_page_layout.addWidget(self.grid_scroll)
        self.grid_stack.addWidget(grid_page)

        self.empty_page = self._create_empty_state()
        self.grid_stack.addWidget(self.empty_page)

        split_layout.addWidget(library_surface, 1)

        # Pannello dettagli dentro una scrollarea per evitare accavallamenti
        details_panel = self.create_details_panel()
        details_scroll = QScrollArea()
        details_scroll.setWidgetResizable(True)
        details_scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        details_scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        details_scroll.setWidget(details_panel)
        details_scroll.setMinimumWidth(320)
        details_scroll.setMaximumWidth(390)

        split_layout.addWidget(details_scroll)
        layout.addLayout(split_layout, 1)

        return page

    def _create_empty_state(self) -> QWidget:
        page = QWidget()
        page.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(8)
        layout.addStretch()

        icon = QLabel()
        icon.setPixmap(make_icon("image", "#657286", 46).pixmap(46, 46))
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon)

        empty_library_text = self.translations.get("empty_library", "La libreria è vuota") if self.translations else "La libreria è vuota"
        self.empty_title = QLabel(empty_library_text)
        self.empty_title.setObjectName("emptyTitle")
        self.empty_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.empty_title)

        self.empty_text = QLabel(
            "Aggiungi un file GIF, PNG, WEBP o APNG per iniziare."
        )
        self.empty_text.setObjectName("emptyText")
        self.empty_text.setWordWrap(True)
        self.empty_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.empty_text)

        empty_add_first_text = self.translations.get("empty_add_first", "Aggiungi il primo personaggio") if self.translations else "Aggiungi il primo personaggio"
        empty_add = QPushButton(empty_add_first_text)
        empty_add.setProperty("class", "primary")
        empty_add.setIcon(make_icon("add", "#FFFFFF", 16))
        empty_add.setIconSize(QSize(16, 16))
        empty_add.clicked.connect(self.add_character_from_pc)
        layout.addWidget(empty_add, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        return page

    def create_details_panel(self) -> QWidget:
        panel = QFrame()
        panel.setObjectName("detailsPanel")
        panel.setMinimumWidth(320)
        add_shadow(panel, blur=28, y_offset=6, alpha=60)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(14)

        # Header con stato
        header = QHBoxLayout()
        header.setSpacing(8)
        details_eyebrow_text = self.translations.get("details_eyebrow", "DETTAGLI") if self.translations else "DETTAGLI"
        eyebrow = QLabel(details_eyebrow_text)
        eyebrow.setObjectName("panelEyebrow")
        header.addWidget(eyebrow)
        header.addStretch()
        details_not_selected_text = self.translations.get("details_not_selected", "NON SELEZIONATO") if self.translations else "NON SELEZIONATO"
        self.status_badge = QLabel(details_not_selected_text)
        self.status_badge.setObjectName("statusBadge")
        self.status_badge.setProperty("status", "none")
        header.addWidget(self.status_badge)
        layout.addLayout(header)

        # Preview grande centrata
        self.large_preview = QLabel()
        self.large_preview.setFixedSize(150, 150)
        self.large_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.large_preview.setPixmap(draw_placeholder_icon(150, 150, 0.30))
        self.large_preview.setStyleSheet("background: rgba(8, 12, 22, 0.75); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px;")
        layout.addWidget(self.large_preview, 0, Qt.AlignmentFlag.AlignCenter)

        # Nome e pulsante rinomina
        name_row = QHBoxLayout()
        name_row.setSpacing(10)
        no_character_text = self.translations.get("no_character", "Nessun personaggio") if self.translations else "Nessun personaggio"
        self.character_name_label = QLabel(no_character_text)
        self.character_name_label.setObjectName("characterName")
        self.character_name_label.setWordWrap(True)
        name_row.addWidget(self.character_name_label, 1)

        rename_text = self.translations.get("btn_rename", "Rinomina") if self.translations else "Rinomina"
        self.rename_button = QPushButton(rename_text)
        self.rename_button.setIcon(make_icon("edit", "#FFFFFF", 14))
        self.rename_button.setIconSize(QSize(14, 14))
        self.rename_button.setMinimumWidth(85)
        self.rename_button.clicked.connect(self.rename_character)
        name_row.addWidget(self.rename_button)
        layout.addLayout(name_row)

        # Pulsante primario Desktop
        launch_text = self.translations.get("btn_launch_desktop", "Avvia sul desktop") if self.translations else "Avvia sul desktop"
        self.put_button = QPushButton(launch_text)
        self.put_button.setProperty("class", "primary")
        self.put_button.setIcon(make_icon("play", "#FFFFFF", 16))
        self.put_button.setIconSize(QSize(16, 16))
        self.put_button.setMinimumHeight(40)
        self.put_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.put_button.clicked.connect(self.put_character)
        layout.addWidget(self.put_button)

        remove_desktop_text = self.translations.get("btn_remove_desktop", "Rimuovi dal desktop") if self.translations else "Rimuovi dal desktop"
        self.take_button = QPushButton(remove_desktop_text)
        self.take_button.setProperty("class", "secondary")
        self.take_button.setIcon(make_icon("stop", "#DCE4F0", 16))
        self.take_button.setIconSize(QSize(16, 16))
        self.take_button.setMinimumHeight(40)
        self.take_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.take_button.clicked.connect(self.take_character)
        layout.addWidget(self.take_button)

        # Divisore sottile ed elegante
        div1 = QFrame()
        div1.setFixedHeight(1)
        div1.setStyleSheet("background: rgba(255, 255, 255, 0.06); border: none;")
        layout.addWidget(div1)

        # Sezione Comportamento
        behavior_container = QVBoxLayout()
        behavior_container.setSpacing(6)
        behavior_text = self.translations.get("details_behavior", "COMPORTAMENTO") if self.translations else "COMPORTAMENTO"
        behavior_label = QLabel(behavior_text)
        behavior_label.setObjectName("fieldLabel")
        behavior_container.addWidget(behavior_label)

        self.behavior_combo = NoScrollComboBox()
        self.behavior_combo.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        behavior_static_text = self.translations.get("behavior_static", "Statico") if self.translations else "Statico"
        behavior_random_text = self.translations.get("behavior_random_edge", "Bordi casuali") if self.translations else "Bordi casuali"
        behavior_free_text = self.translations.get("behavior_free_walk", "Movimento libero (Sopra Taskbar)") if self.translations else "Movimento libero (Sopra Taskbar)"
        behavior_gravity_text = self.translations.get("behavior_gravity", "Gravità") if self.translations else "Gravità"
        self.behavior_combo.addItem(behavior_static_text, "static")
        self.behavior_combo.addItem(behavior_random_text, "random_edge")
        self.behavior_combo.addItem(behavior_free_text, "free_walk")
        self.behavior_combo.addItem(behavior_gravity_text, "gravity")
        self.behavior_combo.currentIndexChanged.connect(self.on_behavior_changed)
        behavior_container.addWidget(self.behavior_combo)

        # Pulsante lock/click-through
        lock_text = self.translations.get("btn_lock", "Click-through (Bloccato)") if self.translations else "Click-through (Bloccato)"
        self.lock_button = QPushButton(lock_text)
        self.lock_button.setCheckable(True)
        self.lock_button.setProperty("class", "secondary")
        self.lock_button.setIcon(make_icon("lock", "#DCE4F0", 15))
        self.lock_button.setIconSize(QSize(15, 15))
        self.lock_button.clicked.connect(self.on_lock_changed)
        behavior_container.addWidget(self.lock_button)
        layout.addLayout(behavior_container)

        # Sezione Dimensioni & FPS (Input numerico con tastiera e frecce!)
        settings_row = QHBoxLayout()
        settings_row.setSpacing(12)

        fps_container = QVBoxLayout()
        fps_container.setSpacing(6)
        fps_text = self.translations.get("details_fps", "FRAME RATE (FPS)") if self.translations else "FRAME RATE (FPS)"
        fps_label = QLabel(fps_text)
        fps_label.setObjectName("fieldLabel")
        fps_container.addWidget(fps_label)

        self.fps_spin = NoScrollSpinBox()
        self.fps_spin.setRange(1, 60)
        self.fps_spin.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.fps_spin.setValue(30)
        self.fps_spin.setSuffix(" FPS")
        self.fps_spin.valueChanged.connect(self.on_fps_changed)
        fps_container.addWidget(self.fps_spin)
        settings_row.addLayout(fps_container)

        scale_container = QVBoxLayout()
        scale_container.setSpacing(6)
        size_text = self.translations.get("details_size", "DIMENSIONE") if self.translations else "DIMENSIONE"
        scale_label = QLabel(size_text)
        scale_label.setObjectName("fieldLabel")
        scale_container.addWidget(scale_label)

        self.scale_spin = NoScrollSpinBox()
        self.scale_spin.setRange(25, 200)
        self.scale_spin.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.scale_spin.setValue(100)
        self.scale_spin.setSuffix("%")
        self.scale_spin.valueChanged.connect(self.on_scale_changed)
        scale_container.addWidget(self.scale_spin)
        settings_row.addLayout(scale_container)

        layout.addLayout(settings_row)

        # Sezione Strumenti AI
        ai_container = QVBoxLayout()
        ai_container.setSpacing(6)
        ai_header = QLabel("STRUMENTI GRAFICA & AI")
        ai_header.setObjectName("fieldLabel")
        ai_container.addWidget(ai_header)

        remove_bg_text = self.translations.get("btn_remove_bg", "Rimuovi sfondo con AI") if self.translations else "Rimuovi sfondo con AI"
        self.remove_bg_button = QPushButton(remove_bg_text)
        self.remove_bg_button.setProperty("class", "secondary")
        self.remove_bg_button.clicked.connect(self.on_remove_background)
        ai_container.addWidget(self.remove_bg_button)

        restore_text = self.translations.get("btn_restore", "Ripristina originale") if self.translations else "Ripristina originale"
        self.restore_original_button = QPushButton(restore_text)
        self.restore_original_button.setProperty("class", "secondary")
        self.restore_original_button.clicked.connect(self.on_restore_original)
        self.restore_original_button.setVisible(False)
        ai_container.addWidget(self.restore_original_button)
        layout.addLayout(ai_container)

        # Sezione Audio
        audio_container = QVBoxLayout()
        audio_container.setSpacing(6)
        audio_text = self.translations.get("details_audio", "EFFETTI AUDIO") if self.translations else "EFFETTI AUDIO"
        audio_label = QLabel(audio_text)
        audio_label.setObjectName("fieldLabel")
        audio_container.addWidget(audio_label)

        audio_row = QHBoxLayout()
        audio_row.setSpacing(8)
        no_audio_text = self.translations.get("no_audio", "Nessun audio") if self.translations else "Nessun audio"
        self.audio_path_label = QLabel(no_audio_text)
        self.audio_path_label.setObjectName("audioPathLabel")
        self.audio_path_label.setWordWrap(True)
        audio_row.addWidget(self.audio_path_label, 1)

        choose_text = self.translations.get("btn_choose", "Scegli") if self.translations else "Scegli"
        self.audio_browse_button = QPushButton(choose_text)
        self.audio_browse_button.setProperty("class", "secondary")
        self.audio_browse_button.setMinimumWidth(72)
        self.audio_browse_button.clicked.connect(self.on_audio_browse)
        audio_row.addWidget(self.audio_browse_button)
        audio_container.addLayout(audio_row)

        volume_container = QVBoxLayout()
        volume_container.setSpacing(4)
        volume_text = self.translations.get("details_volume", "VOLUME") if self.translations else "VOLUME"
        volume_label = QLabel(volume_text)
        volume_label.setObjectName("fieldLabel")
        volume_container.addWidget(volume_label)
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.valueChanged.connect(self.on_volume_changed)
        volume_container.addWidget(self.volume_slider)
        audio_container.addLayout(volume_container)

        layout.addLayout(audio_container)

        layout.addStretch()

        # Pulsante Elimina in basso
        remove_text = self.translations.get("btn_remove", "Elimina personaggio dalla libreria") if self.translations else "Elimina personaggio dalla libreria"
        self.remove_button = QPushButton(remove_text)
        self.remove_button.setProperty("class", "danger")
        self.remove_button.setIcon(make_icon("trash", "#FB7185", 16))
        self.remove_button.setIconSize(QSize(16, 16))
        self.remove_button.clicked.connect(self.remove_character)
        layout.addWidget(self.remove_button)

        self._set_details_enabled(False)
        return panel

    def create_settings_tab(self) -> QWidget:
        # Crea scroll area per le impostazioni
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # Container widget per il contenuto
        page = QWidget()
        page.setObjectName("settingsPage")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 24, 30, 28)
        layout.setSpacing(16)

        intro = QFrame()
        intro.setObjectName("settingsCard")
        intro_layout = QHBoxLayout(intro)
        intro_layout.setContentsMargins(22, 20, 22, 20)
        intro_layout.setSpacing(14)

        icon = QLabel()
        icon.setFixedSize(42, 42)
        icon.setPixmap(make_icon("settings", "#F2A93B", 28).pixmap(28, 28))
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setStyleSheet(
            "background: #312411; border: 1px solid #55401F; border-radius: 11px;"
        )

        intro_layout.addWidget(icon)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(3)
        settings_title = self.translations.get("launcher_settings_title", "Impostazioni dell'applicazione") if self.translations else "Impostazioni dell'applicazione"
        title = QLabel(settings_title)
        title.setObjectName("sectionTitle")
        settings_desc = self.translations.get("launcher_settings_desc", "Questa sezione è pronta per ospitare preferenze globali, avvio automatico e opzioni grafiche.") if self.translations else "Questa sezione è pronta per ospitare preferenze globali, avvio automatico e opzioni grafiche."
        description = QLabel(settings_desc)
        description.setObjectName("sectionCaption")
        description.setWordWrap(True)
        text_layout.addWidget(title)
        text_layout.addWidget(description)
        intro_layout.addLayout(text_layout, 1)

        coming_soon_text = self.translations.get("launcher_coming_soon", "IN ARRIVO") if self.translations else "IN ARRIVO"
        badge = QLabel(coming_soon_text)
        badge.setObjectName("comingSoonBadge")
        intro_layout.addWidget(badge, 0, Qt.AlignmentFlag.AlignTop)
        layout.addWidget(intro)

        # Sezione Avvio e sistema
        startup_card = QFrame()
        startup_card.setObjectName("settingsCard")
        startup_layout = QVBoxLayout(startup_card)
        startup_layout.setContentsMargins(20, 17, 20, 17)
        startup_layout.setSpacing(12)

        startup_title_text = self.translations.get("launcher_startup_system", "Avvio e sistema") if self.translations else "Avvio e sistema"
        startup_title = QLabel(startup_title_text)
        startup_title.setObjectName("sectionTitle")
        startup_layout.addWidget(startup_title)

        # Toggle Avvia con Windows
        autostart_text = self.translations.get("settings_autostart", "Avvia con Windows") if self.translations else "Avvia con Windows"
        self.autostart_checkbox = QCheckBox(autostart_text)
        self.autostart_checkbox.setObjectName("settingsCheckbox")
        self.autostart_checkbox.toggled.connect(self.on_autostart_changed)
        startup_layout.addWidget(self.autostart_checkbox)

        # Toggle Avvia minimizzato
        start_minimized_text = self.translations.get("settings_start_minimized", "Avvia minimizzato") if self.translations else "Avvia minimizzato"
        self.start_minimized_checkbox = QCheckBox(start_minimized_text)
        self.start_minimized_checkbox.setObjectName("settingsCheckbox")
        self.start_minimized_checkbox.toggled.connect(self.on_start_minimized_changed)
        startup_layout.addWidget(self.start_minimized_checkbox)

        # Language selector
        language_label = QLabel(self.translations.get("settings_language", "Lingua") if self.translations else "Lingua")
        language_label.setObjectName("fieldLabel")
        startup_layout.addWidget(language_label)

        self.language_combo = NoScrollComboBox()
        self.language_combo.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        italian_text = self.translations.get("language_italian", "Italiano") if self.translations else "Italiano"
        english_text = self.translations.get("language_english", "English") if self.translations else "English"
        self.language_combo.addItem(italian_text, "it")
        self.language_combo.addItem(english_text, "en")

        # Blocca segnale durante inizializzazione per evitare prompt di riavvio all'avvio
        self.language_combo.blockSignals(True)

        # Imposta lingua corrente da config
        current_language = self.config_manager.get_global_setting("language", "it")
        for i in range(self.language_combo.count()):
            if self.language_combo.itemData(i) == current_language:
                self.language_combo.setCurrentIndex(i)
                break

        # Sblocca segnale e connetti dopo l'inizializzazione
        self.language_combo.blockSignals(False)
        self.language_combo.currentIndexChanged.connect(self.on_language_changed)
        startup_layout.addWidget(self.language_combo)

        # Comportamento alla chiusura
        close_behavior_text = self.translations.get("settings_close_behavior", "Comportamento alla chiusura:") if self.translations else "Comportamento alla chiusura:"
        close_label = QLabel(close_behavior_text)
        close_label.setObjectName("fieldLabel")
        startup_layout.addWidget(close_label)

        self.close_behavior_combo = NoScrollComboBox()
        self.close_behavior_combo.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        minimize_tray_text = self.translations.get("settings_minimize_tray", "Minimizza in tray") if self.translations else "Minimizza in tray"
        close_app_text = self.translations.get("settings_close_app", "Chiudi l'app") if self.translations else "Chiudi l'app"
        self.close_behavior_combo.addItem(minimize_tray_text, "minimize_to_tray")
        self.close_behavior_combo.addItem(close_app_text, "exit")
        self.close_behavior_combo.currentIndexChanged.connect(self.on_close_behavior_changed)
        startup_layout.addWidget(self.close_behavior_combo)

        layout.addWidget(startup_card)

        # Sezione Aspetto
        appearance_card = QFrame()
        appearance_card.setObjectName("settingsCard")
        appearance_layout = QVBoxLayout(appearance_card)
        appearance_layout.setContentsMargins(20, 17, 20, 17)
        appearance_layout.setSpacing(12)

        appearance_title_text = self.translations.get("launcher_appearance", "Aspetto") if self.translations else "Aspetto"
        appearance_title = QLabel(appearance_title_text)
        appearance_title.setObjectName("sectionTitle")
        appearance_layout.addWidget(appearance_title)

        # Tema con nomi
        theme_text = self.translations.get("settings_theme", "Tema:") if self.translations else "Tema:"
        theme_label = QLabel(theme_text)
        theme_label.setObjectName("fieldLabel")
        appearance_layout.addWidget(theme_label)

        theme_row = QHBoxLayout()
        theme_row.setSpacing(9)

        self.style_a_btn_name = QPushButton("Cyber Aura")
        self.style_a_btn_name.setCheckable(True)
        self.style_a_btn_name.setProperty("class", "secondary")
        self.style_a_btn_name.clicked.connect(lambda: self.on_style_changed("A"))
        theme_row.addWidget(self.style_a_btn_name)

        self.style_b_btn_name = QPushButton("Deep Abyss")
        self.style_b_btn_name.setCheckable(True)
        self.style_b_btn_name.setProperty("class", "secondary")
        self.style_b_btn_name.clicked.connect(lambda: self.on_style_changed("B"))
        theme_row.addWidget(self.style_b_btn_name)

        self.style_c_btn_name = QPushButton("Neon Violet")
        self.style_c_btn_name.setCheckable(True)
        self.style_c_btn_name.setProperty("class", "secondary")
        self.style_c_btn_name.clicked.connect(lambda: self.on_style_changed("C"))
        theme_row.addWidget(self.style_c_btn_name)

        appearance_layout.addLayout(theme_row)

        # Dimensione griglia
        grid_size_text = self.translations.get("settings_grid_size", "Dimensione griglia:") if self.translations else "Dimensione griglia:"
        grid_label = QLabel(grid_size_text)
        grid_label.setObjectName("fieldLabel")
        appearance_layout.addWidget(grid_label)

        self.grid_size_combo = NoScrollComboBox()
        self.grid_size_combo.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        grid_small_text = self.translations.get("grid_small", "Piccola") if self.translations else "Piccola"
        grid_medium_text = self.translations.get("grid_medium", "Media") if self.translations else "Media"
        grid_large_text = self.translations.get("grid_large", "Grande") if self.translations else "Grande"
        self.grid_size_combo.addItem(grid_small_text, "small")
        self.grid_size_combo.addItem(grid_medium_text, "medium")
        self.grid_size_combo.addItem(grid_large_text, "large")
        self.grid_size_combo.currentIndexChanged.connect(self.on_grid_size_changed)
        appearance_layout.addWidget(self.grid_size_combo)

        layout.addWidget(appearance_card)

        # Sezione Comportamento overlay
        overlay_card = QFrame()
        overlay_card.setObjectName("settingsCard")
        overlay_layout = QVBoxLayout(overlay_card)
        overlay_layout.setContentsMargins(20, 17, 20, 17)
        overlay_layout.setSpacing(12)

        overlay_behavior_text = self.translations.get("settings_overlay_behavior", "Comportamento overlay") if self.translations else "Comportamento overlay"
        overlay_title = QLabel(overlay_behavior_text)
        overlay_title.setObjectName("sectionTitle")
        overlay_layout.addWidget(overlay_title)

        # Toggle Pausa automatica in giochi fullscreen
        fullscreen_pause_text = self.translations.get("settings_fullscreen_pause", "Pausa automatica in giochi fullscreen") if self.translations else "Pausa automatica in giochi fullscreen"
        self.fullscreen_pause_checkbox = QCheckBox(fullscreen_pause_text)
        self.fullscreen_pause_checkbox.setObjectName("settingsCheckbox")
        self.fullscreen_pause_checkbox.toggled.connect(self.on_fullscreen_pause_changed)
        overlay_layout.addWidget(self.fullscreen_pause_checkbox)

        # Hotkey globale
        hotkey_text = self.translations.get("settings_hotkey", "Hotkey globale (mostra/nascondi):") if self.translations else "Hotkey globale (mostra/nascondi):"
        hotkey_label = QLabel(hotkey_text)
        hotkey_label.setObjectName("fieldLabel")
        overlay_layout.addWidget(hotkey_label)

        hotkey_row = QHBoxLayout()
        self.hotkey_display = QLabel("Ctrl+Alt+H")
        self.hotkey_display.setObjectName("hotkeyDisplay")
        hotkey_row.addWidget(self.hotkey_display)
        hotkey_row.addStretch()
        overlay_layout.addLayout(hotkey_row)

        # Comportamento predefinito
        default_behavior_text = self.translations.get("settings_default_behavior", "Comportamento predefinito:") if self.translations else "Comportamento predefinito:"
        default_behavior_label = QLabel(default_behavior_text)
        default_behavior_label.setObjectName("fieldLabel")
        overlay_layout.addWidget(default_behavior_label)

        self.default_behavior_combo = NoScrollComboBox()
        self.default_behavior_combo.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        behavior_static_text = self.translations.get("behavior_static", "Statico") if self.translations else "Statico"
        behavior_random_text = self.translations.get("behavior_random_edge", "Bordi casuali") if self.translations else "Bordi casuali"
        behavior_free_text = self.translations.get("behavior_free_walk", "Movimento libero") if self.translations else "Movimento libero"
        behavior_gravity_text = self.translations.get("behavior_gravity", "Gravità") if self.translations else "Gravità"
        self.default_behavior_combo.addItem(behavior_static_text, "static")
        self.default_behavior_combo.addItem(behavior_random_text, "random_edge")
        self.default_behavior_combo.addItem(behavior_free_text, "free_walk")
        self.default_behavior_combo.addItem(behavior_gravity_text, "gravity")
        self.default_behavior_combo.currentIndexChanged.connect(self.on_default_behavior_changed)
        overlay_layout.addWidget(self.default_behavior_combo)

        # FPS predefinito
        default_fps_text = self.translations.get("settings_default_fps", "FPS predefinito:") if self.translations else "FPS predefinito:"
        default_fps_label = QLabel(default_fps_text)
        default_fps_label.setObjectName("fieldLabel")
        overlay_layout.addWidget(default_fps_label)

        self.default_fps_spin = NoScrollSpinBox()
        self.default_fps_spin.setRange(1, 60)
        self.default_fps_spin.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.default_fps_spin.setValue(24)
        self.default_fps_spin.valueChanged.connect(self.on_default_fps_changed)
        overlay_layout.addWidget(self.default_fps_spin)

        layout.addWidget(overlay_card)

        # Sezione Prestazioni
        performance_card = QFrame()
        performance_card.setObjectName("settingsCard")
        performance_layout = QVBoxLayout(performance_card)
        performance_layout.setContentsMargins(20, 17, 20, 17)
        performance_layout.setSpacing(12)

        performance_text = self.translations.get("settings_performance", "Prestazioni") if self.translations else "Prestazioni"
        performance_title = QLabel(performance_text)
        performance_title.setObjectName("sectionTitle")
        performance_layout.addWidget(performance_title)

        # Limite FPS globale
        global_fps_text = self.translations.get("settings_global_fps", "Limite FPS globale (0 = nessun limite):") if self.translations else "Limite FPS globale (0 = nessun limite):"
        global_fps_label = QLabel(global_fps_text)
        global_fps_label.setObjectName("fieldLabel")
        performance_layout.addWidget(global_fps_label)

        self.global_fps_spin = NoScrollSpinBox()
        self.global_fps_spin.setRange(0, 60)
        self.global_fps_spin.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.global_fps_spin.setValue(0)
        no_limit_text = self.translations.get("no_limit", "Nessun limite") if self.translations else "Nessun limite"
        self.global_fps_spin.setSpecialValueText(no_limit_text)
        self.global_fps_spin.valueChanged.connect(self.on_global_fps_changed)
        performance_layout.addWidget(self.global_fps_spin)

        # Cartella personaggi
        folder_text = self.translations.get("settings_folder", "Cartella personaggi:") if self.translations else "Cartella personaggi:"
        folder_label = QLabel(folder_text)
        folder_label.setObjectName("fieldLabel")
        performance_layout.addWidget(folder_label)

        folder_row = QHBoxLayout()
        from src.utils import get_app_data_dir
        self.folder_path_label = QLabel(os.path.join(get_app_data_dir(), "characters"))
        self.folder_path_label.setObjectName("folderPath")
        self.folder_path_label.setWordWrap(True)
        folder_row.addWidget(self.folder_path_label, 1)

        open_folder_text = self.translations.get("btn_open_folder", "Apri cartella") if self.translations else "Apri cartella"
        self.open_folder_button = QPushButton(open_folder_text)
        self.open_folder_button.setProperty("class", "secondary")
        self.open_folder_button.setMaximumWidth(100)
        self.open_folder_button.clicked.connect(self.on_open_folder)
        folder_row.addWidget(self.open_folder_button)

        performance_layout.addLayout(folder_row)

        layout.addWidget(performance_card)

        # Sezione Informazioni
        info_card = QFrame()
        info_card.setObjectName("settingsCard")
        info_layout = QVBoxLayout(info_card)
        info_layout.setContentsMargins(20, 17, 20, 17)
        info_layout.setSpacing(12)

        info_title_text = self.translations.get("info_title", "Informazioni") if self.translations else "Informazioni"
        info_title = QLabel(info_title_text)
        info_title.setObjectName("sectionTitle")
        info_layout.addWidget(info_title)

        version_text = self.translations.get("info_version", "Versione: 1.0.1") if self.translations else "Versione: 1.0.1"
        version_label = QLabel(version_text)
        version_label.setObjectName("infoText")
        info_layout.addWidget(version_label)

        project_text = self.translations.get("info_project", "Aura Layer - Desktop Overlay") if self.translations else "Aura Layer - Desktop Overlay"
        project_label = QLabel(project_text)
        project_label.setObjectName("infoText")
        info_layout.addWidget(project_label)

        credits_text = self.translations.get("info_credits", "Progettato per migliorare la tua esperienza desktop") if self.translations else "Progettato per migliorare la tua esperienza desktop"
        credits_label = QLabel(credits_text)
        credits_label.setObjectName("infoText")
        credits_label.setWordWrap(True)
        info_layout.addWidget(credits_label)

        layout.addWidget(info_card)

        layout.addStretch()

        # Imposta page come widget della scroll area
        scroll.setWidget(page)
        return scroll

    def on_style_changed(self, style: str) -> None:
        """Gestisce il cambio di stile dell'interfaccia."""
        StyleManager.set_style(style)

        # Aggiorna stato pulsanti
        self.style_a_btn_name.setChecked(style == "A")
        self.style_b_btn_name.setChecked(style == "B")
        self.style_c_btn_name.setChecked(style == "C")

        # Ricarica stylesheet
        self.setStyleSheet(StyleManager.stylesheet())

        # Salva preferenza
        self.config_manager.set_global_setting("style", style)

    def on_autostart_changed(self, checked: bool) -> None:
        """Gestisce il toggle Avvia con Windows."""
        import os
        import sys

        try:
            # Percorso cartella Avvio
            startup_folder = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup")

            # Percorso dell'eseguibile corrente (o main.py per sviluppo)
            if getattr(sys, 'frozen', False):
                # Eseguibile compilato
                exe_path = sys.executable
            else:
                # Sviluppo: crea batch che lancia python main.py
                main_py_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py")
                batch_path = os.path.join(os.path.dirname(main_py_path), "start_aura_layer.bat")
                with open(batch_path, 'w') as f:
                    f.write(f'@echo off\npython "{main_py_path}"\n')
                exe_path = batch_path

            shortcut_path = os.path.join(startup_folder, "Aura Layer.lnk")

            if checked:
                # Crea scorciatoia
                import win32com.client
                shell = win32com.client.Dispatch("WScript.Shell")
                shortcut = shell.CreateShortCut(shortcut_path)
                shortcut.Targetpath = exe_path
                shortcut.WorkingDirectory = os.path.dirname(exe_path)
                shortcut.Description = "Aura Layer - Desktop Overlay"
                shortcut.save()
            else:
                # Rimuovi scorciatoia
                if os.path.exists(shortcut_path):
                    os.remove(shortcut_path)

            self.config_manager.set_global_setting("autostart", checked)
        except Exception as e:
            # Se fallisce, rimuovi il checkbox e mostra errore
            self.autostart_checkbox.blockSignals(True)
            self.autostart_checkbox.setChecked(not checked)
            self.autostart_checkbox.blockSignals(False)
            error_text = self.translations.get("msg_error", "Errore") if self.translations else "Errore"
            autostart_failed_text = self.translations.get("dialog_autostart_failed", "Impossibile configurare l'avvio automatico") if self.translations else "Impossibile configurare l'avvio automatico"
            QMessageBox.warning(self, error_text, f"{autostart_failed_text}: {e}")

    def on_start_minimized_changed(self, checked: bool) -> None:
        """Gestisce il toggle Avvia minimizzato."""
        self.config_manager.set_global_setting("start_minimized", checked)

    def on_close_behavior_changed(self, index: int) -> None:
        """Gestisce il cambio di comportamento alla chiusura."""
        behavior = self.close_behavior_combo.itemData(index)
        self.config_manager.set_global_setting("close_behavior", behavior)

    def on_grid_size_changed(self, index: int) -> None:
        """Gestisce il cambio di dimensione griglia."""
        size = self.grid_size_combo.itemData(index)
        self.config_manager.set_global_setting("grid_size", size)
        # Ricrea la griglia con le nuove dimensioni
        self.update_grid()

    def on_fullscreen_pause_changed(self, checked: bool) -> None:
        """Gestisce il toggle Pausa automatica in giochi fullscreen."""
        self.config_manager.set_global_setting("fullscreen_pause", checked)

    def on_default_behavior_changed(self, index: int) -> None:
        """Gestisce il cambio di comportamento predefinito."""
        behavior = self.default_behavior_combo.itemData(index)
        self.config_manager.set_global_setting("default_behavior", behavior)

    def on_default_fps_changed(self, value: int) -> None:
        """Gestisce il cambio di FPS predefinito."""
        self.config_manager.set_global_setting("default_fps", value)

    def on_global_fps_changed(self, value: int) -> None:
        """Gestisce il cambio di limite FPS globale."""
        self.config_manager.set_global_setting("global_fps_limit", value)
        self.global_fps_changed.emit(value)

    def on_language_changed(self, index: int) -> None:
        """Gestisce il cambio di lingua."""
        language = self.language_combo.itemData(index)
        current_language = self.config_manager.get_global_setting("language", "it")

        # Non fare nulla se la lingua non è cambiata
        if language == current_language:
            return

        self.config_manager.set_global_setting("language", language)

        # Mostra messaggio di conferma e riavvia
        restart_text = self.translations.get("msg_language_restart", "Il cambio lingua richiede il riavvio dell'applicazione.") if self.translations else "Il cambio lingua richiede il riavvio dell'applicazione."
        restart_question = self.translations.get("msg_restart_question", "Vuoi riavviare ora?") if self.translations else "Vuoi riavviare ora?"
        info_text = self.translations.get("msg_completed", "Completato") if self.translations else "Completato"

        reply = QMessageBox.question(
            self,
            info_text,
            restart_text + "\n\n" + restart_question,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Emetti segnale di riavvio
            self.quit_requested.emit()

    def on_open_folder(self) -> None:
        """Apre la cartella personaggi con Esplora risorse."""
        import subprocess
        import os
        from src.utils import get_app_data_dir
        folder_path = os.path.join(get_app_data_dir(), "characters")
        subprocess.Popen(f'explorer "{folder_path}"')

    def initialize_style_selector(self) -> None:
        """Inizializza il selettore di stile con la preferenza salvata."""
        saved_style = self.config_manager.get_global_setting("style", "A")
        StyleManager.set_style(saved_style)
        self.style_a_btn_name.setChecked(saved_style == "A")
        self.style_b_btn_name.setChecked(saved_style == "B")
        self.style_c_btn_name.setChecked(saved_style == "C")

    def initialize_settings(self) -> None:
        """Inizializza tutte le impostazioni con i valori salvati."""
        # Avvio e sistema
        autostart = self.config_manager.get_global_setting("autostart", False)
        self.autostart_checkbox.setChecked(autostart)

        start_minimized = self.config_manager.get_global_setting("start_minimized", False)
        self.start_minimized_checkbox.setChecked(start_minimized)

        # Language
        language = self.config_manager.get_global_setting("language", "it")
        index = self.language_combo.findData(language)
        if index >= 0:
            self.language_combo.setCurrentIndex(index)

        close_behavior = self.config_manager.get_global_setting("close_behavior", "minimize_to_tray")
        index = self.close_behavior_combo.findData(close_behavior)
        if index >= 0:
            self.close_behavior_combo.setCurrentIndex(index)

        # Aspetto
        grid_size = self.config_manager.get_global_setting("grid_size", "medium")
        index = self.grid_size_combo.findData(grid_size)
        self.grid_size_combo.blockSignals(True)
        if index >= 0:
            self.grid_size_combo.setCurrentIndex(index)
        self.grid_size_combo.blockSignals(False)

        # Comportamento overlay
        fullscreen_pause = self.config_manager.get_global_setting("fullscreen_pause", False)
        self.fullscreen_pause_checkbox.setChecked(fullscreen_pause)

        default_behavior = self.config_manager.get_global_setting("default_behavior", "static")
        index = self.default_behavior_combo.findData(default_behavior)
        if index >= 0:
            self.default_behavior_combo.setCurrentIndex(index)

        default_fps = self.config_manager.get_global_setting("default_fps", 24)
        self.default_fps_spin.setValue(default_fps)

        # Prestazioni
        global_fps = self.config_manager.get_global_setting("global_fps_limit", 0)
        self.global_fps_spin.setValue(global_fps)

    # -------------------------------------------------------------- Libreria
    def load_characters(self) -> None:
        self.character_manager.load_all_characters()
        self.update_grid()

    def update_grid(self) -> None:
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                if isinstance(item.widget(), CharacterCard):
                    item.widget().cleanup_movie()
                item.widget().setParent(None)
                item.widget().deleteLater()

        self.character_cards.clear()
        characters = self.character_manager.get_all_characters()

        # Ottieni dimensione griglia dalle impostazioni
        grid_size = self.config_manager.get_global_setting("grid_size", "medium")

        if not characters:
            # Mostra messaggio quando la libreria è vuota
            empty_widget = QWidget()
            empty_layout = QVBoxLayout(empty_widget)
            empty_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Icona
            icon_label = QLabel()
            icon_label.setPixmap(make_icon("folder", StyleManager.COLORS["text_dim"], 64).pixmap(64, 64))
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_layout.addWidget(icon_label)

            # Testo
            empty_no_chars_text = self.translations.get("empty_no_characters", "Nessun personaggio ancora") if self.translations else "Nessun personaggio ancora"
            title_label = QLabel(empty_no_chars_text)
            title_label.setObjectName("emptyTitle")
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_layout.addWidget(title_label)

            empty_add_text = self.translations.get("empty_add_pc", "Clicca Aggiungi da PC per iniziare") if self.translations else "Clicca Aggiungi da PC per iniziare"
            subtitle_label = QLabel(empty_add_text)
            subtitle_label.setObjectName("emptySubtitle")
            subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            subtitle_label.setWordWrap(True)
            empty_layout.addWidget(subtitle_label)

            self.grid_layout.addWidget(empty_widget, 0, 0)
        else:
            for name, character in characters.items():
                card = CharacterCard(
                    name,
                    character.character_path,
                    character.get_animation_path(),
                    parent=self.grid_widget,
                    active=name in self.active_characters,
                    grid_size=grid_size,
                    translations=self.translations,
                )
                card.clicked.connect(self.on_character_selected)
                self.character_cards[name] = card

        self.update_counters()
        self._reflow_grid()

    def update_counters(self) -> None:
        """Aggiorna tutti i contatori nel launcher."""
        total = len(self.character_cards)
        active = len(self.active_characters)

        # Aggiorna stats e contatori
        if hasattr(self, "total_stat_value"):
            self.total_stat_value.setText(str(total))
        if hasattr(self, "active_stat_value"):
            self.active_stat_value.setText(str(active))
        if hasattr(self, "sidebar_active_stat"):
            self.sidebar_active_stat.setText(
                "1 compagno attivo" if active == 1 else f"{active} compagni attivi"
            )

        # Aggiorna top bar counter
        self.active_counter.setText(
            "1 attivo" if active == 1 else f"{active} attivi"
        )

        # Aggiorna library count
        self.library_count_label.setText(
            "1 elemento" if total == 1 else f"{total} elementi"
        )

        if self.selected_character not in self.character_cards:
            self.selected_character = None
            self._reset_details_panel()
        elif self.selected_character:
            self.character_cards[self.selected_character].set_selected(True)

        self._reflow_grid()

    def _reflow_grid(self) -> None:
        if not hasattr(self, "grid_layout"):
            return

        while self.grid_layout.count():
            self.grid_layout.takeAt(0)

        names = [
            name
            for name in self.character_cards
            if self.current_filter in name.casefold()
        ]

        names.sort(key=str.casefold, reverse=self.current_sort == "za")

        available_width = max(200, self.grid_scroll.viewport().width() - 8)
        # Ottieni dimensione griglia dalle impostazioni
        grid_size = self.config_manager.get_global_setting("grid_size", "medium")
        card_width, _ = CharacterCard.CARD_SIZES.get(grid_size, CharacterCard.CARD_SIZES["medium"])
        cell_width = card_width + self.grid_layout.horizontalSpacing()
        columns = max(1, available_width // cell_width)

        for index, name in enumerate(names):
            row, column = divmod(index, columns)
            card = self.character_cards[name]
            card.setVisible(True)
            self.grid_layout.addWidget(card, row, column)

        for name, card in self.character_cards.items():
            if name not in names:
                card.setVisible(False)

        if names:
            self.grid_stack.setCurrentIndex(0)
        else:
            self.grid_stack.setCurrentIndex(1)
            if self.current_filter:
                no_results_text = self.translations.get("search_no_results", "Nessun risultato") if self.translations else "Nessun risultato"
                self.empty_title.setText(no_results_text)
                no_results_desc_text = self.translations.get("search_no_results_desc", "Non è stato trovato alcun personaggio per") if self.translations else "Non è stato trovato alcun personaggio per"
                self.empty_text.setText(
                    f"{no_results_desc_text} \"{self.search_bar.text().strip()}\"."
                )
            else:
                empty_library_text = self.translations.get("empty_library", "La libreria è vuota") if self.translations else "La libreria è vuota"
                self.empty_title.setText(empty_library_text)
                add_files_text = self.translations.get("search_add_files", "Aggiungi un file GIF, PNG, WEBP o APNG per iniziare.") if self.translations else "Aggiungi un file GIF, PNG, WEBP o APNG per iniziare."
                self.empty_text.setText(add_files_text)

        total = len(self.character_cards)
        visible = len(names)
        if self.current_filter:
            results_count_text = self.translations.get("search_results_count", "risultati su") if self.translations else "risultati su"
            self.library_count_label.setText(
                f"{visible} {results_count_text} {total}"
                if visible != 1
                else f"1 {results_count_text} {total}"
            )
        else:
            self.library_count_label.setText(
                "1 elemento" if total == 1 else f"{total} elementi"
            )

    def filter_characters(self, text: str) -> None:
        self.current_filter = text.strip().casefold()
        self._reflow_grid()

    def _on_sort_changed(self) -> None:
        self.current_sort = self.sort_combo.currentData() or "az"
        self._reflow_grid()

    def _get_character_backup_path(self, character) -> Optional[str]:
        """Trova il percorso del backup dell'immagine originale, se esistente su disco o in config."""
        if not character or not os.path.isdir(character.character_path):
            return None

        # 1. Controlla se specificato nel file config.json
        backup_file = character.config.get("backup_file")
        if backup_file:
            path = os.path.join(character.character_path, backup_file)
            if os.path.exists(path):
                return path

        # 2. Cerca file che terminano per _backup.<ext> nella cartella del personaggio
        try:
            for item in os.listdir(character.character_path):
                name, ext = os.path.splitext(item)
                if name.endswith("_backup") and ext.lower() in [".gif", ".png", ".webp", ".apng", ".jpg", ".jpeg"]:
                    return os.path.join(character.character_path, item)
        except OSError:
            pass

        # 3. Fallback alla mappa in memoria
        if hasattr(self, '_backup_paths') and character.name in self._backup_paths:
            mem_path = self._backup_paths[character.name]
            if os.path.exists(mem_path):
                return mem_path

        return None

    def on_character_selected(self, character_name: str) -> None:
        character = self.character_manager.get_character(character_name)
        if not character:
            return

        # Ricarica il config per avere i dati più recenti
        character.load_config()

        self.selected_character = character_name
        for name, card in self.character_cards.items():
            card.set_selected(name == character_name)

        self.character_name_label.setText(character_name)

        behavior_index = self.behavior_combo.findData(character.behavior)
        self.behavior_combo.blockSignals(True)
        self.behavior_combo.setCurrentIndex(max(0, behavior_index))
        self.behavior_combo.blockSignals(False)

        self.fps_spin.blockSignals(True)
        self.fps_spin.setValue(character.fps or 30)
        self.fps_spin.blockSignals(False)

        self.scale_spin.blockSignals(True)
        self.scale_spin.setValue(character.scale or 100)
        self.scale_spin.blockSignals(False)

        self.lock_button.blockSignals(True)
        self.lock_button.setChecked(character.locked)
        unlock_text = self.translations.get("btn_unlock", "Sblocca") if self.translations else "Sblocca"
        lock_text = self.translations.get("btn_lock", "Blocca") if self.translations else "Blocca"
        self.lock_button.setText(unlock_text if character.locked else lock_text)
        self.lock_button.blockSignals(False)

        # Aggiorna controlli audio
        if character.has_audio():
            self.audio_path_label.setText(character.audio_file)
            self.audio_path_label.setStyleSheet("color: {};".format(StyleManager.COLORS["text"]))
        else:
            self.audio_path_label.setText("Nessun audio")
            self.audio_path_label.setStyleSheet("")

        self.volume_slider.blockSignals(True)
        self.volume_slider.setValue(int(character.volume * 100))
        self.volume_slider.blockSignals(False)

        # Mostra/nascondi pulsante ripristina se esiste backup
        backup_path = self._get_character_backup_path(character)
        self.restore_original_button.setVisible(backup_path is not None)

        # Pulisci movie precedente se esiste
        if self.details_movie:
            self.details_movie.stop()
            self.large_preview.setMovie(None)
            self.details_movie = None

        animation_path = character.get_animation_path()
        if animation_path.lower().endswith(".gif"):
            self.details_movie = QMovie(animation_path)
            if self.details_movie.isValid():
                self.details_movie.setScaledSize(QSize(150, 150))
                self.large_preview.setMovie(self.details_movie)
                self.details_movie.start()
            else:
                thumbnail = load_thumbnail(animation_path, 150, 150, 12)
                self.large_preview.setPixmap(
                    thumbnail
                    if thumbnail is not None
                    else draw_placeholder_icon(150, 150, 0.30)
                )
        else:
            thumbnail = load_thumbnail(animation_path, 150, 150, 12)
            self.large_preview.setPixmap(
                thumbnail
                if thumbnail is not None
                else draw_placeholder_icon(150, 150, 0.30)
            )

        self._set_details_enabled(True)
        self.update_button_states()
        self.character_selected.emit(character_name)

    def _set_details_enabled(self, enabled: bool) -> None:
        self.behavior_combo.setEnabled(enabled)
        self.fps_spin.setEnabled(enabled)
        self.scale_spin.setEnabled(enabled)
        self.lock_button.setEnabled(enabled)
        self.audio_browse_button.setEnabled(enabled)
        self.volume_slider.setEnabled(enabled)
        self.remove_bg_button.setEnabled(enabled)
        self.restore_original_button.setEnabled(enabled)
        self.put_button.setEnabled(enabled)
        self.take_button.setEnabled(False)
        self.rename_button.setEnabled(enabled)
        self.remove_button.setEnabled(enabled)

    def _reset_details_panel(self) -> None:
        if not hasattr(self, "character_name_label"):
            return

        self.character_name_label.setText("Nessun personaggio")
        self.large_preview.setPixmap(draw_placeholder_icon(150, 150, 0.30))
        self.status_badge.setText("NON SELEZIONATO")
        self.status_badge.setProperty("status", "none")
        repolish(self.status_badge)

        # Resetta lock_button
        self.lock_button.blockSignals(True)
        self.lock_button.setChecked(False)
        self.lock_button.setText("Blocca")
        self.lock_button.blockSignals(False)

        # Resetta controlli audio
        self.audio_path_label.setText("Nessun audio")
        self.audio_path_label.setStyleSheet("")
        self.volume_slider.blockSignals(True)
        self.volume_slider.setValue(50)
        self.volume_slider.blockSignals(False)

        self._set_details_enabled(False)

    # --------------------------------------------------------------- Azioni
    def add_character_from_pc(self) -> None:
        dialog_select_animation_text = self.translations.get("dialog_select_animation", "Seleziona animazione") if self.translations else "Seleziona animazione"
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            dialog_select_animation_text,
            "",
            "File animazione (*.gif *.png *.webp *.apng)",
        )

        if not file_path:
            return

        character_name = os.path.splitext(os.path.basename(file_path))[
            0
        ].strip()
        characters_dir = self.character_manager.characters_dir
        character_path = os.path.join(characters_dir, character_name)

        if os.path.exists(character_path):
            dialog_exists_text = self.translations.get("dialog_character_exists", "Personaggio già presente") if self.translations else "Personaggio già presente"
            dialog_exists_desc_text = self.translations.get("dialog_character_exists_desc", "Esiste già un personaggio con questo nome.") if self.translations else "Esiste già un personaggio con questo nome."
            QMessageBox.warning(self, dialog_exists_text, dialog_exists_desc_text)
            return

        try:
            os.makedirs(character_path)
            destination = os.path.join(
                character_path, os.path.basename(file_path)
            )
            shutil.copy2(file_path, destination)

            config = {
                "name": character_name,
                "animation_file": os.path.basename(file_path),
                "audio_file": None,
                "behavior": "static",
                "width": 200,
                "height": 200,
                "draggable": True,
                "speed": 1.0,
                "volume": 0.5,
                "fps": 30,
                "scale": 100,
                "locked": False,
            }

            with open(
                os.path.join(character_path, "config.json"),
                "w",
                encoding="utf-8",
            ) as file:
                json.dump(config, file, indent=2, ensure_ascii=False)

        except OSError as error:
            if os.path.isdir(character_path):
                shutil.rmtree(character_path, ignore_errors=True)
            import_failed_text = self.translations.get("dialog_import_failed", "Importazione non riuscita") if self.translations else "Importazione non riuscita"
            import_error_text = self.translations.get("dialog_import_error", "Non è stato possibile aggiungere il personaggio.") if self.translations else "Non è stato possibile aggiungere il personaggio."
            QMessageBox.critical(
                self,
                import_failed_text,
                f"{import_error_text}\n\n{error}",
            )
            return

        self.load_characters()
        self.update_counters()
        if character_name in self.character_cards:
            self.on_character_selected(character_name)

    def put_character(self) -> None:
        """Attiva il personaggio selezionato."""
        if not self.selected_character:
            return
        self.character_launched.emit(self.selected_character)

    def take_character(self) -> None:
        """Disattiva il personaggio selezionato."""
        if not self.selected_character:
            return
        self.character_deactivated.emit(self.selected_character)

    def remove_character(self) -> None:
        if not self.selected_character:
            return

        removed_name = self.selected_character
        remove_character_text = self.translations.get("dialog_remove_character", "Rimuovi personaggio") if self.translations else "Rimuovi personaggio"
        remove_confirm_text = self.translations.get("dialog_remove_confirm", "Vuoi rimuovere definitivamente") if self.translations else "Vuoi rimuovere definitivamente"
        reply = QMessageBox.question(
            self,
            remove_character_text,
            f"{remove_confirm_text} \"{removed_name}\" dalla libreria?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        character = self.character_manager.get_character(removed_name)
        try:
            if character and os.path.isdir(character.character_path):
                shutil.rmtree(character.character_path)
        except OSError as error:
            removal_failed_text = self.translations.get("dialog_removal_failed", "Rimozione non riuscita") if self.translations else "Rimozione non riuscita"
            remove_error_text = self.translations.get("dialog_remove_error", "Non è stato possibile rimuovere il personaggio.") if self.translations else "Non è stato possibile rimuovere il personaggio."
            QMessageBox.critical(
                self,
                removal_failed_text,
                f"{remove_error_text}\n\n{error}",
            )
            return

        self.active_characters.discard(removed_name)
        self.selected_character = None
        self.load_characters()
        self.character_removed.emit(removed_name)

    def rename_character(self) -> None:
        if not self.selected_character:
            return

        old_name = self.selected_character
        rename_character_text = self.translations.get("dialog_rename_character", "Rinomina personaggio") if self.translations else "Rinomina personaggio"
        new_name_text = self.translations.get("dialog_new_name", "Nuovo nome:") if self.translations else "Nuovo nome:"
        new_name, accepted = QInputDialog.getText(
            self,
            rename_character_text,
            new_name_text,
            text=old_name,
        )

        new_name = new_name.strip()

        if not accepted or not new_name or new_name == old_name:
            return

        if os.path.basename(new_name) != new_name or new_name in {".", ".."}:
            invalid_name_text = self.translations.get("dialog_invalid_name", "Nome non valido") if self.translations else "Nome non valido"
            invalid_folder_text = self.translations.get("dialog_invalid_folder_chars", "Il nome non può contenere separatori di cartella.") if self.translations else "Il nome non può contenere separatori di cartella."
            QMessageBox.warning(
                self,
                invalid_name_text,
                invalid_folder_text,
            )
            return

        character = self.character_manager.get_character(old_name)
        if not character:
            return

        new_path = os.path.join(
            self.character_manager.characters_dir, new_name
        )
        if os.path.exists(new_path):
            name_used_text = self.translations.get("dialog_name_used", "Nome già utilizzato") if self.translations else "Nome già utilizzato"
            name_used_desc_text = self.translations.get("dialog_name_used_desc", "Esiste già un personaggio con questo nome.") if self.translations else "Esiste già un personaggio con questo nome."
            QMessageBox.warning(self, name_used_text, name_used_desc_text)
            return

        try:
            os.rename(character.character_path, new_path)
            config_path = os.path.join(new_path, "config.json")
            with open(config_path, "r", encoding="utf-8") as file:
                config = json.load(file)
            config["name"] = new_name
            with open(config_path, "w", encoding="utf-8") as file:
                json.dump(config, file, indent=2, ensure_ascii=False)
        except (OSError, json.JSONDecodeError) as error:
            rename_failed_text = self.translations.get("dialog_rename_failed", "Rinomina non riuscita") if self.translations else "Rinomina non riuscita"
            rename_error_text = self.translations.get("dialog_rename_error", "Non è stato possibile rinominare il personaggio.") if self.translations else "Non è stato possibile rinominare il personaggio."
            QMessageBox.critical(
                self,
                rename_failed_text,
                f"{rename_error_text}\n\n{error}",
            )
            return

        if old_name in self.active_characters:
            self.active_characters.remove(old_name)
            self.active_characters.add(new_name)

        self.selected_character = new_name
        self.load_characters()
        if new_name in self.character_cards:
            self.on_character_selected(new_name)
        self.character_renamed.emit(old_name, new_name)

    # ----------------------------------------------------------- Stato/config
    def update_active_characters(self, active_names: list) -> None:
        self.active_characters = set(active_names)
        self._sync_active_states()

    def _sync_active_states(self) -> None:
        for name, card in self.character_cards.items():
            card.set_active(name in self.active_characters)
        self.update_button_states()
        self._update_stats()

    def update_button_states(self) -> None:
        if not self.selected_character:
            return

        is_active = self.selected_character in self.active_characters
        self.put_button.setEnabled(not is_active)
        self.take_button.setEnabled(is_active)

        self.status_badge.setText("ATTIVO" if is_active else "PRONTO")
        self.status_badge.setProperty(
            "status", "active" if is_active else "inactive"
        )
        repolish(self.status_badge)

    def _update_stats(self) -> None:
        total = len(self.character_cards)
        active = len(
            self.active_characters.intersection(self.character_cards.keys())
        )

        self.total_stat_value.setText(str(total))
        self.active_stat_value.setText(str(active))
        self.active_counter.setText(
            "1 personaggio attivo"
            if active == 1
            else f"{active} personaggi attivi"
        )

    def on_behavior_changed(self, value) -> None:
        if not self.selected_character:
            return

        # Accetta sia l'indice emesso dalla nuova combo sia la stringa usata
        # dalla precedente implementazione, così il metodo resta compatibile.
        behavior = (
            value if isinstance(value, str) else self.behavior_combo.currentData()
        )
        character = self.character_manager.get_character(self.selected_character)
        if character and behavior:
            character.update_config(behavior=behavior)
            character.save_config()
            self.character_updated.emit(self.selected_character)

    def on_fps_changed(self, fps: int) -> None:
        if not self.selected_character:
            return

        character = self.character_manager.get_character(self.selected_character)
        if character:
            character.update_config(fps=fps)
            character.save_config()
            self.character_updated.emit(self.selected_character)

    def on_scale_changed(self, scale: int) -> None:
        if not self.selected_character:
            return

        character = self.character_manager.get_character(self.selected_character)
        if character:
            character.update_config(scale=scale)
            character.save_config()
            self.character_updated.emit(self.selected_character)

    def on_lock_changed(self) -> None:
        if not self.selected_character:
            return

        character = self.character_manager.get_character(self.selected_character)
        if not character:
            return

        character.update_config(locked=self.lock_button.isChecked())
        character.save_config()

        # Aggiorna testo pulsante
        if self.lock_button.isChecked():
            unlock_text = self.translations.get("btn_unlock", "Sblocca") if self.translations else "Sblocca"
            self.lock_button.setText(unlock_text)
        else:
            lock_text = self.translations.get("btn_lock", "Blocca") if self.translations else "Blocca"
            self.lock_button.setText(lock_text)

        # Emetti segnale per applicare lock senza riavviare
        self.character_lock_changed.emit(self.selected_character, character.locked)

    def on_audio_browse(self) -> None:
        """Permette all'utente di selezionare un file audio."""
        if not self.selected_character:
            return

        character = self.character_manager.get_character(self.selected_character)
        if not character:
            return

        select_audio_text = self.translations.get("dialog_select_audio", "Seleziona file audio") if self.translations else "Seleziona file audio"
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            select_audio_text,
            "",
            "Audio Files (*.mp3 *.wav *.ogg *.flac);;All Files (*)"
        )

        if file_path:
            # Copia il file nella cartella del personaggio
            try:
                import shutil
                audio_filename = os.path.basename(file_path)
                dest_path = os.path.join(character.character_path, audio_filename)
                shutil.copy2(file_path, dest_path)

                character.update_config(audio_file=audio_filename)
                character.save_config()

                self.audio_path_label.setText(audio_filename)
                self.audio_path_label.setStyleSheet("color: {};".format(StyleManager.COLORS["text"]))
            except Exception as e:
                error_text = self.translations.get("msg_error", "Errore") if self.translations else "Errore"
                audio_copy_failed_text = self.translations.get("dialog_audio_copy_failed", "Impossibile copiare il file audio") if self.translations else "Impossibile copiare il file audio"
                QMessageBox.critical(self, error_text, f"{audio_copy_failed_text}: {e}")

    def on_volume_changed(self, value: int) -> None:
        """Gestisce il cambio del volume."""
        if not self.selected_character:
            return

        character = self.character_manager.get_character(self.selected_character)
        if not character:
            return

        volume = value / 100.0
        character.update_config(volume=volume)
        character.save_config()

    def on_remove_background(self) -> None:
        """Rimuove lo sfondo dall'animazione del personaggio selezionato usando AI."""
        import shutil

        if not self.selected_character:
            return

        character = self.character_manager.get_character(self.selected_character)
        if not character:
            return

        animation_path = character.get_animation_path()
        if not animation_path or not os.path.exists(animation_path):
            error_text = self.translations.get("msg_error", "Errore") if self.translations else "Errore"
            no_animation_text = self.translations.get("dialog_no_animation", "Nessun file di animazione trovato per questo personaggio.") if self.translations else "Nessun file di animazione trovato per questo personaggio."
            QMessageBox.warning(self, error_text, no_animation_text)
            return

        # Verifica formato GIF
        if animation_path.lower().endswith('.gif'):
            warning_text = self.translations.get("msg_warning", "Attenzione") if self.translations else "Attenzione"
            gif_warning_text = self.translations.get("msg_bg_gif_warning", "La rimozione dello sfondo con AI non supporta le GIF animate. L'operazione convertirà la GIF in un'immagine statica. Vuoi continuare?") if self.translations else "La rimozione dello sfondo con AI non supporta le GIF animate. L'operazione convertirà la GIF in un'immagine statica. Vuoi continuare?"
            reply = QMessageBox.warning(
                self,
                warning_text,
                gif_warning_text,
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                return

        # Crea percorsi
        base_path = animation_path.rsplit('.', 1)[0]
        output_path = base_path + '_no_bg.png'
        backup_path = base_path + '_backup' + os.path.splitext(animation_path)[1]

        # Crea backup del file originale se non esiste
        if not os.path.exists(backup_path):
            shutil.copy2(animation_path, backup_path)

        # Disabilita pulsante durante elaborazione
        self.remove_bg_button.setEnabled(False)
        self.remove_bg_button.setText("Elaborazione in corso...")

        # Esegui rimozione sfondo in un thread separato
        class BackgroundRemovalThread(QThread):
            finished = pyqtSignal(bool, str, str)

            def __init__(self, input_path, output_path, backup_path):
                super().__init__()
                self.input_path = input_path
                self.output_path = output_path
                self.backup_path = backup_path

            def run(self):
                try:
                    # Import locale per evitare caricamento lento all'avvio
                    from src.background_remover import BackgroundRemover
                    # Rimuovi sfondo
                    success = BackgroundRemover.remove_background(self.input_path, self.output_path)
                    self.finished.emit(success, self.output_path, self.backup_path)
                except Exception as e:
                    # Cattura qualsiasi eccezione per evitare crash dell'app
                    print(f"Errore durante rimozione sfondo: {e}")
                    self.finished.emit(False, self.output_path, self.backup_path)

        # Salva riferimento al thread per gestirlo correttamente
        if not hasattr(self, '_bg_removal_thread'):
            self._bg_removal_thread = None

        self._bg_removal_thread = BackgroundRemovalThread(animation_path, output_path, backup_path)
        self._bg_removal_thread.finished.connect(lambda success, path, backup: self._on_background_removal_finished(success, path, backup, character))
        self._bg_removal_thread.start()

    def _on_background_removal_finished(self, success: bool, output_path: str, backup_path: str, character) -> None:
        """Callback quando la rimozione dello sfondo è completata."""
        self.remove_bg_button.setEnabled(True)
        remove_bg_text = self.translations.get("btn_remove_bg", "Rimuovi sfondo con AI") if self.translations else "Rimuovi sfondo con AI"
        self.remove_bg_button.setText(remove_bg_text)

        if success:
            # Aggiorna config per usare la nuova immagine e salvare il riferimento persistente al backup
            new_filename = os.path.basename(output_path)
            backup_filename = os.path.basename(backup_path)
            character.update_config(animation_file=new_filename, backup_file=backup_filename)
            character.save_config()

            # Salva percorso del backup anche per la sessione corrente
            if not hasattr(self, '_backup_paths'):
                self._backup_paths = {}
            self._backup_paths[self.selected_character] = backup_path

            # Mostra pulsante ripristina
            self.restore_original_button.setVisible(True)

            # Ricarica anteprima
            self.on_character_selected(self.selected_character)

            # Se il personaggio era attivo sul desktop, notifica il cambio per ricaricarlo
            if self.selected_character in self.active_characters:
                self.character_updated.emit(self.selected_character)

            completed_text = self.translations.get("msg_completed", "Completato") if self.translations else "Completato"
            success_text = self.translations.get("msg_bg_success", "Sfondo rimosso con successo! L'animazione è stata aggiornata.") if self.translations else "Sfondo rimosso con successo! L'animazione è stata aggiornata."
            restore_text = self.translations.get("msg_bg_restore", "Puoi ripristinare l'originale con il pulsante 'Ripristina originale'.") if self.translations else "Puoi ripristinare l'originale con il pulsante 'Ripristina originale'."
            QMessageBox.information(
                self,
                completed_text,
                f"{success_text}\n\n{restore_text}"
            )
        else:
            error_text = self.translations.get("msg_error", "Errore") if self.translations else "Errore"
            bg_error_text = self.translations.get("msg_bg_error", "Impossibile rimuovere lo sfondo. Verifica che il file sia valido.") if self.translations else "Impossibile rimuovere lo sfondo. Verifica che il file sia valido."
            QMessageBox.critical(
                self,
                error_text,
                bg_error_text
            )

    def on_restore_original(self) -> None:
        """Ripristina l'immagine originale dal backup preservando il file senza sfondo."""
        if not self.selected_character:
            return

        character = self.character_manager.get_character(self.selected_character)
        if not character:
            return

        # Verifica se esiste un backup (su disco, in config o in memoria)
        backup_path = self._get_character_backup_path(character)
        if not backup_path or not os.path.exists(backup_path):
            warning_text = self.translations.get("msg_warning", "Attenzione") if self.translations else "Attenzione"
            no_backup_text = self.translations.get("msg_no_backup", "Non esiste un backup dell'originale per questo personaggio.") if self.translations else "Non esiste un backup dell'originale per questo personaggio."
            QMessageBox.warning(self, warning_text, no_backup_text)
            self.restore_original_button.setVisible(False)
            return

        # Conferma ripristino
        restore_title = self.translations.get("btn_restore", "Ripristina originale") if self.translations else "Ripristina originale"
        restore_confirm_text = self.translations.get("msg_restore_confirm", "Vuoi ripristinare l'immagine originale?\n\nL'immagine senza sfondo verrà mantenuta.") if self.translations else "Vuoi ripristinare l'immagine originale?\n\nL'immagine senza sfondo verrà mantenuta."
        reply = QMessageBox.question(
            self,
            restore_title,
            restore_confirm_text,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        try:
            import shutil

            # Determina il nome corretto del file originale dal backup
            backup_filename = os.path.basename(backup_path)
            name_part, ext_part = os.path.splitext(backup_filename)
            if name_part.endswith("_backup"):
                original_filename = name_part[:-7] + ext_part
            else:
                original_filename = backup_filename

            original_dest_path = os.path.join(character.character_path, original_filename)
            # Se il file originale non esiste (o differisce), ripristiniamo dal backup
            if not os.path.exists(original_dest_path):
                shutil.copy2(backup_path, original_dest_path)

            # Aggiorna config per usare l'originale e rimuovere il riferimento al backup
            character.update_config(animation_file=original_filename, backup_file=None)
            character.save_config()

            # Pulisci il riferimento in memoria
            if hasattr(self, '_backup_paths') and self.selected_character in self._backup_paths:
                del self._backup_paths[self.selected_character]
            self.restore_original_button.setVisible(False)

            # Ricarica anteprima
            self.on_character_selected(self.selected_character)

            # Se il personaggio era attivo sul desktop, notifica il cambio per aggiornare l'overlay
            if self.selected_character in self.active_characters:
                self.character_updated.emit(self.selected_character)

            completed_text = self.translations.get("msg_completed", "Completato") if self.translations else "Completato"
            restore_success_text = self.translations.get("dialog_restore_success", "Immagine originale ripristinata con successo!") if self.translations else "Immagine originale ripristinata con successo!"
            QMessageBox.information(
                self,
                completed_text,
                restore_success_text
            )

        except Exception as e:
            error_text = self.translations.get("msg_error", "Errore") if self.translations else "Errore"
            restore_failed_text = self.translations.get("dialog_restore_failed", "Impossibile ripristinare l'originale") if self.translations else "Impossibile ripristinare l'originale"
            QMessageBox.critical(self, error_text, f"{restore_failed_text}: {e}")

    # -------------------------------------------------------------- Finestra
    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        if hasattr(self, "grid_scroll"):
            QTimer.singleShot(0, self._reflow_grid)

    def showEvent(self, event) -> None:
        super().showEvent(event)
        # Ripristina l'animazione di anteprima se presente
        if self.details_movie and self.details_movie.isValid() and self.details_movie.state() != QMovie.MovieState.Running:
            self.details_movie.start()

    def closeEvent(self, event) -> None:
        self.on_close(event)

    def on_close(self, event) -> None:
        event.ignore()

        # Leggi il comportamento alla chiusura
        close_behavior = self.config_manager.get_global_setting("close_behavior", "minimize_to_tray")

        if close_behavior == "exit":
            # Chiudi l'applicazione
            self.quit_requested.emit()
        else:
            # Minimizza in tray e metti in pausa l'anteprima per azzerare il consumo CPU
            if self.details_movie and self.details_movie.state() == QMovie.MovieState.Running:
                self.details_movie.stop()
            self.hide()