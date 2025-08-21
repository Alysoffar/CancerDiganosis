import streamlit as st
import numpy as np
import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler
import datetime
import json
import os
from hashlib import sha256
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import hmac
import hashlib
import sqlite3

# Set page config for better appearance
st.set_page_config(
    page_title="Advanced Medical Diagnosis System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for 3D effects and enhanced styling with new background
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    
    * {
        font-family: 'Roboto', sans-serif;
    }
    
    .main > div {
        padding-top: 2rem;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 25%, #dee2e6 50%, #ced4da 75%, #adb5bd 100%);
        min-height: 100vh;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f1f3f4 0%, #e8eaf6 25%, #e3f2fd 50%, #e0f2f1 75%, #f3e5f5 100%);
        min-height: 100vh;
    }
    
    /* 3D Card Effects */
    .card-3d {
        background: linear-gradient(145deg, #e8e8e8, #d0d0d0);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 
            20px 20px 60px #bebebe,
            -20px -20px 60px #ffffff;
        transform: translateZ(0);
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: #000000 !important;
    }
    
    .card-3d * {
        color: #000000 !important;
    }
    
    .card-3d:hover {
        transform: translateY(-10px) rotateX(5deg);
        box-shadow: 
            25px 25px 80px #bebebe,
            -25px -25px 80px #ffffff;
    }
    
    /* Success Box 3D (grey theme) */
    .success-box-3d {
        background: linear-gradient(145deg, #e8e8e8, #d0d0d0);
        border: 1px solid rgba(255, 255, 255, 0.4);
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 
            0 15px 35px #bebebe,
            inset 0 1px rgba(255, 255, 255, 0.5);
        transform: perspective(1000px) rotateX(2deg);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        color: #000000 !important;
    }
    
    .success-box-3d:hover {
        transform: perspective(1000px) rotateX(0deg) translateZ(5px);
        box-shadow: 
            0 20px 40px #bebebe,
            inset 0 1px rgba(255, 255, 255, 0.6);
    }
    
    .success-box-3d h3, .success-box-3d p, .success-box-3d div {
        color: #000000 !important;
    }
    
    /* 3D Buttons */
    .stButton > button {
        background: linear-gradient(145deg, #e8e8e8, #d0d0d0);
        border: none;
        border-radius: 15px;
        padding: 0.8rem 2rem;
        color: #000000 !important;
        font-weight: 600;
        box-shadow: 
            8px 8px 16px #bebebe,
            -8px -8px 16px #ffffff;
        transition: all 0.3s ease;
        transform: translateZ(0);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 
            12px 12px 24px #bebebe,
            -12px -12px 24px #ffffff;
        background: linear-gradient(145deg, #d0d0d0, #c0c0c0);
    }
    
    .stButton > button:active {
        transform: translateY(1px) scale(0.98);
        box-shadow: 
            4px 4px 8px #bebebe,
            -4px -4px 8px #ffffff;
    }
    
    /* Enhanced Metrics with 3D effect */
    .stMetric {
        background: linear-gradient(145deg, #ffffff, #f0f0f0);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 
            10px 10px 20px #c8ced3,
            -10px -10px 20px #ffffff;
        transform: translateZ(0);
        transition: all 0.3s ease;
        color: #000000 !important;
    }
    
    .stMetric * {
        color: #000000 !important;
    }
    
    .stMetric:hover {
        transform: translateY(-5px);
        box-shadow: 
            15px 15px 30px #c8ced3,
            -15px -15px 30px #ffffff;
    }
    
    /* Success and Warning boxes with 3D effects */
    .success-box-3d {
        background: linear-gradient(145deg, #d4edda, #c3e6cb);
        padding: 2rem;
        border-radius: 20px;
        border-left: 8px solid #28a745;
        margin: 1rem 0;
        box-shadow: 
            15px 15px 30px #a8d4b3,
            -15px -15px 30px #e8f5ea;
        transform: translateZ(0);
        transition: all 0.3s ease;
        color: #155724 !important;
    }
    
    .success-box-3d * {
        color: #155724 !important;
    }
    
    .success-box-3d:hover {
        transform: translateY(-5px) rotateX(2deg);
        box-shadow: 
            20px 20px 40px #a8d4b3,
            -20px -20px 40px #e8f5ea;
    }
    
    .warning-box-3d {
        background: linear-gradient(145deg, #e8e8e8, #d0d0d0);
        padding: 2rem;
        border-radius: 20px;
        border-left: 8px solid #a0a0a0;
        margin: 1rem 0;
        box-shadow: 
            15px 15px 30px #bebebe,
            -15px -15px 30px #ffffff;
        transform: translateZ(0);
        transition: all 0.3s ease;
        color: #000000 !important;
    }
    
    .warning-box-3d * {
        color: #000000 !important;
    }
    
    .warning-box-3d:hover {
        transform: translateY(-5px) rotateX(2deg);
        box-shadow: 
            20px 20px 40px #bebebe,
            -20px -20px 40px #ffffff;
    }
    
    /* Re-establish colored box text after global override */
    .success-box-3d, .success-box-3d * {
        color: #155724 !important;
    }
    
    .warning-box-3d, .warning-box-3d * {
        color: #000000 !important;
    }
    
    /* 3D Input Fields */
    .stNumberInput > div > div > input {
        border-radius: 10px;
        border: 1px solid #ddd;
        box-shadow: inset 4px 4px 8px #d0d0d0, inset -4px -4px 8px #ffffff;
        transition: all 0.3s ease;
    }
    
    .stNumberInput > div > div > input:focus {
        box-shadow: inset 6px 6px 12px #d0d0d0, inset -6px -6px 12px #ffffff;
        border-color: #667eea;
    }
    
    /* 3D Sidebar */
    .css-1d391kg {
        background: linear-gradient(145deg, #d0d0d0, #e0e0e0);
        border-radius: 15px;
        box-shadow: 
            10px 10px 20px #bebebe,
            -10px -10px 20px #ffffff;
    }
    
    /* Sidebar text color - Multiple selectors for better targeting */
    .css-1d391kg, .css-1d391kg * {
        color: #ffffff !important;
    }
    
    /* Streamlit sidebar selectors */
    [data-testid="stSidebar"], [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    /* Additional sidebar selectors */
    .stSidebar, .stSidebar * {
        color: #ffffff !important;
    }
    
    /* Sidebar markdown elements */
    .css-1d391kg .stMarkdown, .css-1d391kg .stMarkdown * {
        color: #ffffff !important;
    }
    
    /* Sidebar button text should remain white */
    .css-1d391kg .stButton button {
        color: #ffffff !important;
    }
    
    /* 3D Title */
    .main-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    /* Patient card styling */
    .patient-card {
        background: linear-gradient(145deg, #ffffff, #f8f9fa);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid #667eea;
        box-shadow: 
            8px 8px 16px #d0d0d0,
            -8px -8px 16px #ffffff;
        transition: all 0.3s ease;
        color: #000000 !important;
    }
    
    .patient-card * {
        color: #000000 !important;
    }
    
    .patient-card:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 
            12px 12px 24px #d0d0d0,
            -12px -12px 24px #ffffff;
    }
    
    /* Login form styling */
    .login-container {
        max-width: 800px;
        margin: 0 auto;
        background: linear-gradient(145deg, #e8e8e8, #d0d0d0);
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 
            20px 20px 40px #bebebe,
            -20px -20px 40px #ffffff;
        transform: translateZ(0);
        color: #000000 !important;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .login-container * {
        color: #000000 !important;
    }
    
    /* Form styling improvements */
    .stTextInput > div > div > input {
        border-radius: 12px !important;
        border: 2px solid #c0c0c0 !important;
        padding: 14px 18px !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        background: #f5f5f5 !important;
        color: #000000 !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #888888 !important;
        box-shadow: 0 0 0 3px rgba(136, 136, 136, 0.1) !important;
        background: #f0f0f0 !important;
    }
    
    .stSelectbox > div > div > select {
        border-radius: 12px !important;
        border: 2px solid #c0c0c0 !important;
        padding: 14px 18px !important;
        font-size: 16px !important;
        background: #f5f5f5 !important;
        color: #000000 !important;
    }
    
    .stSelectbox > div > div > select:focus {
        border-color: #888888 !important;
        background: #f0f0f0 !important;
    }
    
    .stSelectbox > div > div > select option {
        background: #f5f5f5 !important;
        color: #000000 !important;
        padding: 10px !important;
    }
    
    .stNumberInput > div > div > input {
        border-radius: 12px !important;
        border: 2px solid #c0c0c0 !important;
        padding: 14px 18px !important;
        font-size: 16px !important;
        background: #f5f5f5 !important;
        color: #000000 !important;
    }
    
    .stTextArea > div > div > textarea {
        border-radius: 12px !important;
        border: 2px solid #c0c0c0 !important;
        padding: 14px 18px !important;
        font-size: 16px !important;
        background: #f5f5f5 !important;
        color: #000000 !important;
    }
    
    /* Additional Dropdown Fixes */
    .stSelectbox div[data-baseweb="select"] {
        background: #f5f5f5 !important;
        border-radius: 12px !important;
        border: 2px solid #c0c0c0 !important;
    }
    
    .stSelectbox div[data-baseweb="select"] > div {
        background: #f5f5f5 !important;
        color: #000000 !important;
        padding: 14px 18px !important;
        border-radius: 12px !important;
    }
    
    /* Dropdown menu styling */
    .stSelectbox div[role="listbox"] {
        background: #f5f5f5 !important;
        border: 2px solid #c0c0c0 !important;
        border-radius: 12px !important;
    }
    
    .stSelectbox div[role="option"] {
        background: #f5f5f5 !important;
        color: #000000 !important;
        padding: 10px 18px !important;
    }
    
    .stSelectbox div[role="option"]:hover {
        background: #e0e0e0 !important;
        color: #000000 !important;
    }
    
    /* Fix checkbox styling */
    .stCheckbox {
        color: #000000 !important;
    }
    
    .stCheckbox > label {
        color: #000000 !important;
    }
    
    /* Navigation pills */
    .nav-pill {
        background: linear-gradient(145deg, #667eea, #764ba2);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.2rem;
        display: inline-block;
        box-shadow: 
            4px 4px 8px #c8ced3,
            -4px -4px 8px #ffffff;
        transition: all 0.3s ease;
    }
    
    .nav-pill:hover {
        transform: translateY(-2px);
        box-shadow: 
            6px 6px 12px #c8ced3,
            -6px -6px 12px #ffffff;
    }
    
    /* General text color fixes */
    .stApp, .stApp * {
        color: #000000 !important;
    }
    
    /* Ensure all text elements have proper contrast */
    p, span, div, h1, h2, h3, h4, h5, h6 {
        color: #000000 !important;
    }
    
    /* Main content text */
    .main * {
        color: #000000 !important;
    }
    
    /* General text color fixes */
    .stApp, .stApp * {
        color: #000000 !important;
    }
    
    /* Ensure all text elements have proper contrast */
    p, span, div, h1, h2, h3, h4, h5, h6 {
        color: #000000 !important;
    }
    
    /* Main content text */
    .main * {
        color: #000000 !important;
    }
    
    /* Streamlit specific elements */
    .stMarkdown, .stMarkdown * {
        color: #000000 !important;
    }
    
    .stWrite, .stWrite * {
        color: #000000 !important;
    }
    
    /* All Streamlit text elements */
    .stText, .stText * {
        color: #000000 !important;
    }
    
    /* Headers and subheaders */
    .stHeader, .stHeader * {
        color: #000000 !important;
    }
    
    .stSubheader, .stSubheader * {
        color: #000000 !important;
    }
    
    /* Code blocks and preformatted text */
    .stCode, .stCode * {
        color: #000000 !important;
    }
    
    /* All paragraph elements */
    [data-testid="stMarkdownContainer"] p {
        color: #000000 !important;
    }
    
    /* All div elements in main content */
    [data-testid="stVerticalBlock"] div {
        color: #000000 !important;
    }
    
    /* Button text color (grey theme) */
    .stButton > button {
        color: #000000 !important;
    }
    
    /* Input labels and values */
    .stNumberInput label, .stTextInput label, .stSelectbox label, .stTextArea label {
        color: #000000 !important;
    }
    
    .stNumberInput input, .stTextInput input, .stTextArea textarea {
        color: #000000 !important;
        background-color: #f5f5f5 !important;
        border: 2px solid #c0c0c0 !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
    }
    
    /* Selectbox styling - white text for readability */
    .stSelectbox select {
        color: #ffffff !important;
        background-color: #3a3a3a !important;
        border: 2px solid #c0c0c0 !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
    }

    /* Dropdown options - white on dark */
    .stSelectbox select option {
        color: #ffffff !important;
        background-color: #2a2a2a !important;
    }

    /* Target the dropdown container */
    .stSelectbox > div > div {
        color: #ffffff !important;
    }

    /* Target the selected value display */
    .stSelectbox > div > div > div {
        color: #ffffff !important;
        background-color: #3a3a3a !important;
        border-radius: 12px !important;
    }

    /* Additional selectbox targeting */
    [data-testid="stSelectbox"] select,
    [data-testid="stSelectbox"] option {
        color: #ffffff !important;
        background-color: #3a3a3a !important;
    }
    
    /* Target the actual dropdown options when opened (legacy UL/LI) */
    .stSelectbox ul li {
        color: #ffffff !important;
        background-color: #2a2a2a !important;
    }
    
    /* More specific dropdown option targeting (ARIA role) */
    .stSelectbox [role="option"] {
        color: #ffffff !important;
        background-color: #2a2a2a !important;
    }
    .stSelectbox [role="option"]:hover {
        background-color: #444444 !important;
        color: #ffffff !important;
    }
    .stSelectbox [role="option"][aria-selected="true"],
    .stSelectbox [role="option"][data-selected="true"] {
        background-color: #555555 !important;
        color: #ffffff !important;
    }
    
    /* Streamlit/react-select current value & placeholder */
    .css-1wa3eu0-placeholder, .css-1uccc91-singleValue {
        color: #ffffff !important;
    }
    
    /* React-select dropdown menu */
    .css-26l3qy-menu {
        background-color: #2a2a2a !important;
        border: 2px solid #c0c0c0 !important;
        border-radius: 12px !important;
    }
    
    .css-26l3qy-menu .css-1n7v3ny-option {
        color: #ffffff !important;
        background-color: #2a2a2a !important;
    }
    
    .css-26l3qy-menu .css-1n7v3ny-option:hover {
        color: #ffffff !important;
        background-color: #444444 !important;
    }

    /* More specific selectbox selectors (dark) */
    [data-testid="stSelectbox"] div[role="listbox"],
    [data-testid="stSelectbox"] div[role="option"],
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div,
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div > div {
        color: #ffffff !important;
        background-color: #2a2a2a !important;
        border: 2px solid #c0c0c0 !important;
        border-radius: 12px !important;
    }

    /* Target the actual input/display element */
    .stSelectbox input,
    .stSelectbox div[role="combobox"] {
        color: #ffffff !important;
        background-color: #3a3a3a !important;
    }

    /* Metric labels */
    .stMetric .metric-label, 
    .stMetric .metric-value {
        color: #000000 !important;
    }

    /* More targeted approach instead of global override */
    /* Remove the global * selector and target specific elements instead */
    .stApp, .main .block-container, p, span, div:not([data-testid="stSelectbox"] div) {
        color: #000000 !important;
    }

    /* Re-establish button colors */
    .stButton > button, 
    .stDownloadButton > button {
        color: white !important;
        background: linear-gradient(145deg, #667eea, #764ba2) !important;
    }

    /* Ensure selectbox grey theme */
    .stSelectbox, 
    .stSelectbox * {
        color: #000000 !important;
    }
    
    /* Force the dropdown options (Female, Male, Other) to be white */
    div[data-baseweb="select"] > div,
    div[data-baseweb="select"] > div > div,
    div[data-baseweb="select"] ul,
    div[data-baseweb="select"] ul li,
    div[data-baseweb="select"] [role="option"] {
        color: #ffffff !important;
        background-color: rgba(0, 0, 0, 0.8) !important;
    }
    
    /* Target the select dropdown menu specifically */
    .stSelectbox div[data-baseweb="popover"] div[role="listbox"] > div {
        color: #ffffff !important;
        background-color: rgba(0, 0, 0, 0.8) !important;
    }
    
    /* Override any remaining black text in selectbox */
    .stSelectbox div:not(.stSelectbox div[data-testid]) {
        color: #ffffff !important;
    }
    
    /* Target the dropdown menu that appears when clicked */
    .stSelectbox div[role="listbox"] {
        background-color: rgba(0, 0, 0, 0.9) !important;
    }
    
    .stSelectbox div[role="listbox"] > div {
        color: #ffffff !important;
        background-color: rgba(0, 0, 0, 0.8) !important;
    }
    
    /* Target each option in the dropdown list */
    .stSelectbox div[role="option"] {
        color: #ffffff !important;
        background-color: rgba(0, 0, 0, 0.8) !important;
    }
    
    /* Target options on hover */
    .stSelectbox div[role="option"]:hover {
        color: #ffffff !important;
        background-color: rgba(0, 0, 0, 0.9) !important;
    }
    
    /* Additional targeting for the dropdown items */
    .stSelectbox ul[role="listbox"] li,
    .stSelectbox div[data-baseweb="menu"] > div,
    .stSelectbox div[data-baseweb="menu"] > div > div {
        color: #ffffff !important;
        background-color: rgba(0, 0, 0, 0.8) !important;
    }
    
    /* ULTIMATE OVERRIDE - Force all selectbox content to be white */
    div[data-baseweb="select"] * {
        color: #ffffff !important;
    }
    
    /* Target the menu content specifically */
    div[data-baseweb="menu"] * {
        color: #ffffff !important;
        background-color: rgba(0, 0, 0, 0.8) !important;
    }
    
    /* Force override for all selectbox descendants */
    .stSelectbox * {
        color: #ffffff !important;
    }
    
    /* Target specific Streamlit select classes */
    .css-1uccc91-singleValue,
    .css-1wa3eu0-placeholder,
    .css-26l3qy-menu,
    .css-4ljt47-MenuList,
    .css-11unzgr,
    .css-1n7v3ny-option {
        color: #ffffff !important;
        background-color: rgba(0, 0, 0, 0.8) !important;
    }
    
    /* Nuclear option - override everything in selectbox with white */
    .stSelectbox div,
    .stSelectbox span,
    .stSelectbox p,
    .stSelectbox li {
        color: #ffffff !important;
    }

    /* Override any remaining white text */
    * {
        color: #000000 !important;
    }
    
    /* Re-establish button colors after global override */
    .stButton > button, .stDownloadButton > button {
        color: white !important;
        background: linear-gradient(145deg, #667eea, #764ba2) !important;
    }
    
    /* FORCE sidebar text to be white - override the global black rule */
    [data-testid="stSidebar"] *, 
    .css-1d391kg *, 
    .stSidebar *,
    section[data-testid="stSidebar"] *,
    .css-1d391kg h1,
    .css-1d391kg h2, 
    .css-1d391kg h3,
    .css-1d391kg p,
    .css-1d391kg span,
    .css-1d391kg div {
        color: #ffffff !important;
    }
    
    /* Special styling for gender dropdown */
    .stSelectbox select {
        color: #ffffff !important;
        background-color: rgba(0, 0, 0, 0.7) !important;
        font-weight: bold !important;
        border: 2px solid #4CAF50 !important;
    }

    /* Force dropdown text to be white - multiple selectors */
    .stSelectbox select option {
        color: #ffffff !important;
        background-color: rgba(0, 0, 0, 0.8) !important;
    }

    /* Target the dropdown container */
    .stSelectbox > div > div {
        color: #ffffff !important;
    }

    /* Target the selected value display */
    .stSelectbox > div > div > div {
        color: #ffffff !important;
        background-color: rgba(0, 0, 0, 0.7) !important;
    }

    /* Additional selectbox targeting */
    [data-testid="stSelectbox"] select,
    [data-testid="stSelectbox"] option {
        color: #ffffff !important;
        background-color: rgba(0, 0, 0, 0.7) !important;
    }

    /* More specific selectbox selectors to override global styles */
    [data-testid="stSelectbox"] div[role="listbox"],
    [data-testid="stSelectbox"] div[role="option"],
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div,
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div > div {
        color: #ffffff !important;
        background-color: rgba(0, 0, 0, 0.7) !important;
    }

    /* Target the actual input/display element */
    .stSelectbox input,
    .stSelectbox div[role="combobox"] {
        color: #ffffff !important;
        background-color: rgba(0, 0, 0, 0.7) !important;
    }

    /* Metric labels */
    .stMetric .metric-label, 
    .stMetric .metric-value {
        color: #000000 !important;
    }

    /* More targeted approach instead of global override */
    /* Remove the global * selector and target specific elements instead */
    .stApp, .main .block-container, p, span, div:not([data-testid="stSelectbox"] div) {
        color: #000000 !important;
    }

    /* Re-establish button colors */
    .stButton > button, 
    .stDownloadButton > button {
        color: white !important;
        background: linear-gradient(145deg, #667eea, #764ba2) !important;
    }

    /* Ensure selectbox text stays white despite other targeting */
    .stSelectbox, 
    .stSelectbox * {
        color: #ffffff !important;
    }
    /* FORCE sidebar text to be white - override the global black rule */
    [data-testid="stSidebar"] *, 
    .css-1d391kg *, 
    .stSidebar *,
    section[data-testid="stSidebar"] *,
    .css-1d391kg h1,
    .css-1d391kg h2, 
    .css-1d391kg h3,
    .css-1d391kg p,
    .css-1d391kg span,
    .css-1d391kg div {
        color: #ffffff !important;
    }
    
    /* Hide Streamlit progress bars and loading indicators */
    .stProgress > div > div > div > div {
        display: none !important;
    }
    
    .stProgress {
        display: none !important;
    }
    
    /* Hide the running indicator bars */
    .stAppViewContainer > .main > div > .block-container > div > div > div > .stProgress {
        display: none !important;
    }
    
    /* Hide any loading/running bars */
    div[data-testid="stProgress"] {
        display: none !important;
    }
    
    /* Hide the status indicators */
    .statusWidget {
        display: none !important;
    }
    
    /* Hide running app indicators */
    .st-emotion-cache-1dp5vir {
        display: none !important;
    }

    /* Portal-safe overrides to force white text in dropdown menu options */
    div[role="listbox"] {
        background-color: #2a2a2a !important;
        border: 2px solid #c0c0c0 !important;
        border-radius: 12px !important;
    }
    div[role="option"] {
        color: #ffffff !important;
        background-color: #2a2a2a !important;
        padding: 10px 16px !important;
    }
    div[role="option"]:hover {
        background-color: #444444 !important;
        color: #ffffff !important;
    }
    div[role="option"][aria-selected="true"],
    div[role="option"][data-selected="true"] {
        background-color: #555555 !important;
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_doctor' not in st.session_state:
    st.session_state.current_doctor = None
if 'patients_data' not in st.session_state:
    st.session_state.patients_data = {}
if 'show_signup' not in st.session_state:
    st.session_state.show_signup = False
if 'pending_applications' not in st.session_state:
    st.session_state.pending_applications = {}

def _get_secret_key():
    """Obtain secret key for signing approval links."""
    key = None
    try:
        key = st.secrets.get("APP_SECRET_KEY", None)
    except Exception:
        key = None
    if not key:
        key = os.environ.get("APP_SECRET_KEY", "dev-insecure-secret")
    return key.encode()

def _sign_token(app_id: str, action: str) -> str:
    return hmac.new(_get_secret_key(), f"{app_id}:{action}".encode(), hashlib.sha256).hexdigest()

def _verify_token(app_id: str, action: str, token: str) -> bool:
    expected = _sign_token(app_id, action)
    return hmac.compare_digest(expected, token)

def _get_base_url():
    # Allow override via secrets or env, fallback to localhost
    try:
        base_url = st.secrets.get("app_base_url", None)
    except Exception:
        base_url = None
    if not base_url:
        base_url = os.environ.get("APP_BASE_URL", "http://localhost:8501")
    return base_url.rstrip('/')

def _build_action_link(app_id: str, action: str) -> str:
    token = _sign_token(app_id, action)
    base = _get_base_url()
    # Use query params the app will parse on load
    return f"{base}/?app_id={app_id}&action={action}&token={token}"

def send_generic_email(to_addr: str, subject: str, body_html: str):
    """Utility to send an email with existing SMTP configuration."""
    try:
        smtp = {}
        try:
            smtp = st.secrets.get("smtp", {})
        except Exception:
            smtp = {}
        host = smtp.get("host") or os.environ.get("SMTP_HOST")
        if not host:
            st.warning("SMTP host not configured; email skipped.")
            return False
        port = int(smtp.get("port") or os.environ.get("SMTP_PORT") or 587)
        user = smtp.get("user") or os.environ.get("SMTP_USER")
        password = smtp.get("password") or os.environ.get("SMTP_PASSWORD")
        use_tls = smtp.get("use_tls", True)
        use_ssl = smtp.get("use_ssl", False)
        from_addr = smtp.get("from") or user or "no-reply@localhost"

        if not (user and password):
            st.warning("SMTP credentials missing; email skipped.")
            return False

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = from_addr
        msg["To"] = to_addr
        msg.attach(MIMEText(body_html, "html"))

        if use_ssl:
            with smtplib.SMTP_SSL(host, port, timeout=20) as server:
                server.login(user, password)
                server.sendmail(from_addr, [to_addr], msg.as_string())
        else:
            with smtplib.SMTP(host, port, timeout=20) as server:
                server.ehlo()
                if use_tls:
                    server.starttls(); server.ehlo()
                server.login(user, password)
                server.sendmail(from_addr, [to_addr], msg.as_string())
        return True
    except Exception as e:
        st.error(f"Email error: {e}")
        return False

def send_signup_email(doctor_info):
    """Send signup notification email to admin (real SMTP with approval links)."""
    try:
        # Admin receiver fallback
        admin_email = None
        try:
            admin_email = st.secrets.get("admin_email", None)
        except Exception:
            admin_email = None
        if not admin_email:
            admin_email = "alymoh226@gmail.com"

        # Build email content
        subject = f"🏥 New Doctor Registration Request - {doctor_info['name']}"
        body = f"""
        <html>
        <body>
        <h2>🏥 Medical Diagnosis System - New Doctor Registration</h2>

        <p>A new doctor has requested access to the Medical Diagnosis System:</p>

        <div style="background-color: #f0f0f0; padding: 20px; margin: 20px 0; border-radius: 10px;">
            <h3>👨‍⚕️ Doctor Information:</h3>
            <p><strong>Full Name:</strong> {doctor_info['name']}</p>
            <p><strong>Email:</strong> {doctor_info['email']}</p>
            <p><strong>Specialization:</strong> {doctor_info['specialization']}</p>
            <p><strong>License Number:</strong> {doctor_info['license']}</p>
            <p><strong>Hospital/Clinic:</strong> {doctor_info['hospital']}</p>
            <p><strong>Phone Number:</strong> {doctor_info['phone']}</p>
            <p><strong>Years of Experience:</strong> {doctor_info['experience']}</p>
            <p><strong>Requested Username:</strong> {doctor_info['username']}</p>
            <p><strong>Application Date:</strong> {doctor_info['application_date']}</p>
        </div>

        <div style="background-color: #e8f4f8; padding: 15px; margin: 20px 0; border-radius: 8px;">
            <h4>📋 Additional Notes:</h4>
            <p>{doctor_info.get('notes', 'No additional notes provided.')}</p>
        </div>

        <div style="background-color: #fff3cd; padding: 15px; margin: 20px 0; border-radius: 8px; border-left: 4px solid #ffc107;">
            <p><strong>⚠️ Action Required:</strong></p>
            <p>Please review this application and decide whether to grant access to the Medical Diagnosis System.</p>
            <p>You can approve or reject this application by logging into the admin panel.</p>
        </div>

        <hr>
        <p style="color: #666; font-size: 12px;">
        This is an automated message from the Medical Diagnosis System.<br>
        Application ID: {doctor_info['application_id']}<br>
        Timestamp: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        </p>
        </body>
        </html>
        """

        # Prepare SMTP configuration: st.secrets first, then environment variables
        smtp = {}
        try:
            smtp = st.secrets.get("smtp", {})
        except Exception:
            smtp = {}

        host = smtp.get("host") or os.environ.get("SMTP_HOST")
        port = int(smtp.get("port") or os.environ.get("SMTP_PORT") or 587)
        user = smtp.get("user") or os.environ.get("SMTP_USER")
        password = smtp.get("password") or os.environ.get("SMTP_PASSWORD")
        use_tls = smtp.get("use_tls", True)
        use_ssl = smtp.get("use_ssl", False)
        from_addr = smtp.get("from") or user
        to_addr = smtp.get("to") or admin_email

        # Build the MIME email
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = from_addr or (user or "no-reply@localhost")
        msg["To"] = to_addr
        msg.attach(MIMEText(body, "html"))

        sent = False
        if host and user and password:
            if use_ssl:
                with smtplib.SMTP_SSL(host, port, timeout=20) as server:
                    server.login(user, password)
                    server.sendmail(msg["From"], [to_addr], msg.as_string())
                    sent = True
            else:
                with smtplib.SMTP(host, port, timeout=20) as server:
                    server.ehlo()
                    if use_tls:
                        server.starttls()
                        server.ehlo()
                    server.login(user, password)
                    server.sendmail(msg["From"], [to_addr], msg.as_string())
                    sent = True
        else:
            st.warning("Email not sent: missing SMTP configuration (host/user/password). Add [smtp] in secrets or set SMTP_* environment variables.")

        # Store the application (in a real app, this would go to a database)
        app_id = doctor_info.get('application_id') or f"APP_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        doctor_info['application_id'] = app_id
        # Persist pending application to DB
        try:
            db_store_pending(doctor_info)
        except Exception as e:
            st.error(f"Failed to store pending application: {e}")

        # Append approval / rejection links if we can build them
        approve_link = _build_action_link(app_id, 'accept')
        reject_link = _build_action_link(app_id, 'reject')
        links_block = f"<p><strong>Quick Actions:</strong><br>✅ <a href='{approve_link}'>Approve</a> &nbsp; | &nbsp; ❌ <a href='{reject_link}'>Reject</a></p>"
        body_with_links = body.replace('</body>', f'{links_block}</body>')

        # Replace body in existing message (rebuild msg for clarity)
        # Reconstruct MIME with links
        # (We reuse same msg variable logic above; easier to just rebuild and resend if not sent yet.)

        # If already sent earlier above we would need to embed before send, but we only send once below.
        # Adjust the earlier code so we only send now with links.
        # For simplicity: re-build message and re-send using generic helper if not sent yet.

        # Use generic sending path (ensures single send with links)
        # We'll bypass the earlier 'sent' variable path by resetting it and sending again.
        # NOTE: This slight restructure ensures links are included.

        # We will ignore previously built msg & resend with links.

        # Prepare final message with links using send_generic_email for consistency
        if host and user and password:  # Variables from earlier scope
            # Rebuild final message using helper
            final_sent = send_generic_email(to_addr, subject, body_with_links)
            sent = final_sent

        if sent:
            st.success("✅ Application submitted and email sent to admin.")
            return True
        else:
            st.info("📦 Application saved locally. Configure SMTP to enable outgoing email.")
            return False

    except Exception as e:
        st.error(f"❌ Error sending application: {str(e)}")
        return False

# Legacy DOCTORS dict retained only for backward compatibility; primary source is DB
DOCTORS = {}

# Load trained model and scaler
@st.cache_resource
def load_models():
    try:
        model = joblib.load("breast_cancer_model.pkl")
        scaler = joblib.load("scaler.pkl")
        return model, scaler
    except FileNotFoundError as e:
        st.error(f"Model or scaler file not found: {e}")
        st.error("Please train and save both the model and scaler first.")
        st.stop()

model, scaler = load_models()

# Feature names matching the dataset
feature_names = [
    "radius_mean", "texture_mean", "perimeter_mean", "area_mean", "smoothness_mean",
    "compactness_mean", "concavity_mean", "concave_points_mean", "symmetry_mean", "fractal_dimension_mean",
    "radius_se", "texture_se", "perimeter_se", "area_se", "smoothness_se",
    "compactness_se", "concavity_se", "concave_points_se", "symmetry_se", "fractal_dimension_se",
    "radius_worst", "texture_worst", "perimeter_worst", "area_worst", "smoothness_worst",
    "compactness_worst", "concavity_worst", "concave_points_worst", "symmetry_worst", "fractal_dimension_worst"
]

DB_PATH = "medical_app.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            username TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT,
            specialization TEXT,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS pending_applications (
            application_id TEXT PRIMARY KEY,
            username TEXT,
            name TEXT,
            email TEXT,
            phone TEXT,
            specialization TEXT,
            experience TEXT,
            license TEXT,
            hospital TEXT,
            password_hash TEXT,
            notes TEXT,
            application_date TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            patient_id TEXT PRIMARY KEY,
            doctor_username TEXT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            diagnosis TEXT,
            prediction TEXT,
            confidence REAL,
            created_at TEXT,
            features_json TEXT,
            proba_json TEXT,
            treatment_plan TEXT,
            progress_json TEXT
        )
    """)
    # Seed initial doctors if empty
    cur.execute("SELECT COUNT(*) FROM doctors")
    if cur.fetchone()[0] == 0:
        seed = [
            ("dr.smith", "Dr. John Smith", None, "Oncology", sha256("medical123".encode()).hexdigest()),
            ("dr.jones", "Dr. Sarah Jones", None, "Radiology", sha256("health456".encode()).hexdigest()),
            ("dr.wilson", "Dr. Michael Wilson", None, "Pathology", sha256("cancer789".encode()).hexdigest())
        ]
        cur.executemany("INSERT INTO doctors (username,name,email,specialization,password_hash) VALUES (?,?,?,?,?)", seed)
    conn.commit(); conn.close()

@st.cache_resource
def ensure_db():
    init_db(); return True

ensure_db()

def db_get_doctor(username: str):
    conn = sqlite3.connect(DB_PATH); cur = conn.cursor()
    cur.execute("SELECT username,name,email,specialization,password_hash FROM doctors WHERE username=?", (username,))
    row = cur.fetchone(); conn.close()
    if row:
        return {"username": row[0], "name": row[1], "email": row[2], "specialization": row[3], "password": row[4]}
    return None

def db_insert_doctor(info: dict):
    conn = sqlite3.connect(DB_PATH); cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO doctors (username,name,email,specialization,password_hash) VALUES (?,?,?,?,?)",
                (info['username'], info['name'], info.get('email'), info.get('specialization'), info['password']))
    conn.commit(); conn.close()

def db_store_pending(app: dict):
    conn = sqlite3.connect(DB_PATH); cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO pending_applications (application_id,username,name,email,phone,specialization,experience,license,hospital,password_hash,notes,application_date) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (app['application_id'], app['username'], app['name'], app['email'], app.get('phone'), app.get('specialization'), app.get('experience'), app.get('license'), app.get('hospital'), app['password'], app.get('notes'), app.get('application_date')))
    conn.commit(); conn.close()

def db_get_pending(application_id: str):
    conn = sqlite3.connect(DB_PATH); cur = conn.cursor()
    cur.execute("SELECT application_id,username,name,email,phone,specialization,experience,license,hospital,password_hash,notes,application_date FROM pending_applications WHERE application_id=?", (application_id,))
    row = cur.fetchone(); conn.close()
    if row:
        keys = ["application_id","username","name","email","phone","specialization","experience","license","hospital","password","notes","application_date"]
        return dict(zip(keys, row))
    return None

def db_delete_pending(application_id: str):
    conn = sqlite3.connect(DB_PATH); cur = conn.cursor(); cur.execute("DELETE FROM pending_applications WHERE application_id=?", (application_id,)); conn.commit(); conn.close()

# ---------------- Patients Persistence -----------------
def db_upsert_patient(doctor_username: str, patient_id: str, data: dict):
    conn = sqlite3.connect(DB_PATH); cur = conn.cursor()
    cur.execute("""
        INSERT INTO patients (patient_id, doctor_username, name, age, gender, diagnosis, prediction, confidence, created_at, features_json, proba_json, treatment_plan, progress_json)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(patient_id) DO UPDATE SET
            doctor_username=excluded.doctor_username,
            name=excluded.name,
            age=excluded.age,
            gender=excluded.gender,
            diagnosis=excluded.diagnosis,
            prediction=excluded.prediction,
            confidence=excluded.confidence,
            created_at=excluded.created_at,
            features_json=excluded.features_json,
            proba_json=excluded.proba_json,
            treatment_plan=excluded.treatment_plan,
            progress_json=excluded.progress_json
    """,
        (
            patient_id,
            doctor_username,
            data.get('name'),
            data.get('age'),
            data.get('gender'),
            data.get('diagnosis'),
            data.get('prediction'),
            data.get('confidence'),
            data.get('date'),
            json.dumps(data.get('features', {})),
            json.dumps(data.get('proba', [])),
            data.get('treatment_plan', ''),
            json.dumps(data.get('progress', []))
        )
    )
    conn.commit(); conn.close()

def db_get_patients_for_doctor(doctor_username: str) -> dict:
    conn = sqlite3.connect(DB_PATH); cur = conn.cursor()
    cur.execute("SELECT patient_id, name, age, gender, diagnosis, prediction, confidence, created_at, features_json, proba_json, treatment_plan, progress_json FROM patients WHERE doctor_username=?", (doctor_username,))
    rows = cur.fetchall(); conn.close()
    patients = {}
    for r in rows:
        patients[r[0]] = {
            'name': r[1], 'age': r[2], 'gender': r[3], 'diagnosis': r[4], 'prediction': r[5], 'confidence': r[6], 'date': r[7],
            'features': json.loads(r[8]) if r[8] else {},
            'proba': json.loads(r[9]) if r[9] else [],
            'treatment_plan': r[10] or '',
            'progress': json.loads(r[11]) if r[11] else []
        }
    return patients

def load_doctor_patients_into_session(username: str):
    try:
        st.session_state.patients_data = db_get_patients_for_doctor(username)
    except Exception as e:
        st.warning(f"Could not load patients: {e}")

def authenticate_user(username, password):
    doc = db_get_doctor(username)
    if doc and doc['password'] == sha256(password.encode()).hexdigest():
        return doc
    return None

def save_patient_data(patient_id, patient_data):
    """Save patient data to session state"""
    st.session_state.patients_data[patient_id] = patient_data
    # Persist to DB if doctor context available
    try:
        doctor_username = st.session_state.get('username')
        if doctor_username:
            db_upsert_patient(doctor_username, patient_id, patient_data)
    except Exception as e:
        st.warning(f"Could not persist patient {patient_id}: {e}")

def get_patient_data(patient_id):
    """Get patient data from session state"""
    return st.session_state.patients_data.get(patient_id, None)

def _doctor_count():
    try:
        conn = sqlite3.connect(DB_PATH); cur = conn.cursor(); cur.execute("SELECT COUNT(*) FROM doctors"); c = cur.fetchone()[0]; conn.close(); return c
    except Exception:
        return 0

def _plot_pie(dist_df):
    try:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(3.2,3.2))
        ax.pie(dist_df['count'], labels=dist_df['prediction'], autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        return fig
    except Exception as e:
        st.warning(f"Pie chart unavailable: {e}")
        return None

def login_page():
    """Display login page"""
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<h1 class="main-title" style="text-align: center;">🏥 Medical Diagnosis System</h1>', unsafe_allow_html=True)
        
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<h3 style="text-align: center; margin-bottom: 30px;">🔐 Doctor Login</h3>', unsafe_allow_html=True)
        
        # Login form
        with st.form("login_form"):
            username = st.text_input("👤 Username", placeholder="Enter your username")
            password = st.text_input("🔐 Password", type="password", placeholder="Enter your password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            login_button = st.form_submit_button("🚀 Login", use_container_width=True)
            
            if login_button:
                if username and password:
                    # Authenticate using central helper
                    user = authenticate_user(username.lower(), password)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.username = username.lower()
                        st.session_state.current_doctor = user
                        load_doctor_patients_into_session(st.session_state.username)
                        st.success("✅ Login successful! Patients loaded.")
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password")
                else:
                    st.error("❌ Please enter both username and password")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Signup option - centered
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
        
        if st.button("📝 New Doctor? Apply for Access", key="show_signup_btn", use_container_width=True):
            st.session_state.show_signup = True
            st.rerun()
        
        st.markdown("**Don't have an account?** Click above to apply for system access.")
        st.markdown('</div>', unsafe_allow_html=True)

def signup_page():
    """Display doctor registration/signup page - completely separate from login"""
    # Center the signup form
    col1, col2, col3 = st.columns([0.5, 3, 0.5])
    
    with col2:
        st.markdown('<h1 class="main-title" style="text-align: center;">👨‍⚕️ Doctor Registration</h1>', unsafe_allow_html=True)
        
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<h3 style="text-align: center; color: #4A90E2; margin-bottom: 20px;">📝 Apply for System Access</h3>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; margin-bottom: 30px;">Please fill out this form to request access to the Medical Diagnosis System.</p>', unsafe_allow_html=True)
        
        with st.form("doctor_signup_form"):
            # Personal Information
            st.markdown("#### 👤 Personal Information")
            col_left, col_right = st.columns(2)
            
            with col_left:
                full_name = st.text_input("Full Name *", placeholder="Dr. John Smith")
                email = st.text_input("Email Address *", placeholder="doctor@hospital.com")
                phone = st.text_input("Phone Number *", placeholder="+1 (555) 123-4567")
            
            with col_right:
                specialization = st.selectbox("Medical Specialization *", [
                    "Select Specialization",
                    "Oncology", 
                    "Radiology", 
                    "Pathology",
                    "Internal Medicine",
                    "Surgery",
                    "Cardiology",
                    "Dermatology",
                    "Neurology",
                    "Pediatrics",
                    "Psychiatry",
                    "Emergency Medicine",
                    "Family Medicine",
                    "Other"
                ])
                experience = st.number_input("Years of Experience *", min_value=0, max_value=50, value=0)
                license_number = st.text_input("Medical License Number *", placeholder="MD123456")
            
            # Professional Information
            st.markdown("#### 🏥 Professional Information")
            hospital = st.text_input("Hospital/Clinic Name *", placeholder="General Hospital")
            
            # Login Credentials
            st.markdown("#### 🔐 Requested Login Credentials")
            col_user, col_pass = st.columns(2)
            with col_user:
                username = st.text_input("Preferred Username *", placeholder="dr.smith")
            with col_pass:
                password = st.text_input("Password *", type="password", placeholder="Create a strong password")
                confirm_password = st.text_input("Confirm Password *", type="password", placeholder="Confirm your password")
            
            # Additional Information
            st.markdown("#### 📋 Additional Information")
            notes = st.text_area("Additional Notes (Optional)", 
                                placeholder="Any additional information you'd like to provide...",
                                height=100)
            
            # Terms and Conditions
            st.markdown("#### ⚖️ Terms and Agreement")
            terms_agreed = st.checkbox("I agree that the information provided is accurate and I will use this system responsibly for medical purposes only.")
            
            # Submit button
            st.markdown("<br>", unsafe_allow_html=True)
            col_submit1, col_submit2, col_submit3 = st.columns([1, 2, 1])
            with col_submit2:
                submitted = st.form_submit_button("🚀 Submit Application", use_container_width=True)
            
            if submitted:
                # Validation
                errors = []
                
                if not full_name or len(full_name) < 3:
                    errors.append("Please enter a valid full name")
                
                if not email or "@" not in email:
                    errors.append("Please enter a valid email address")
                
                if specialization == "Select Specialization":
                    errors.append("Please select your medical specialization")
                
                if not license_number or len(license_number) < 3:
                    errors.append("Please enter your medical license number")
                
                if not hospital or len(hospital) < 3:
                    errors.append("Please enter your hospital/clinic name")
                
                if not username or len(username) < 3:
                    errors.append("Please enter a username (minimum 3 characters)")
                
                if not password or len(password) < 6:
                    errors.append("Please enter a password (minimum 6 characters)")
                
                if password != confirm_password:
                    errors.append("Passwords do not match")
                
                if not phone or len(phone) < 10:
                    errors.append("Please enter a valid phone number")
                
                if experience < 0:
                    errors.append("Please enter valid years of experience")
                
                if not terms_agreed:
                    errors.append("Please agree to the terms and conditions")
                
                # Check if username already exists
                # Check existing username in DB
                if db_get_doctor(username.lower()) is not None:
                    errors.append("Username already exists, please choose another one")
                
                if errors:
                    for error in errors:
                        st.error(f"❌ {error}")
                else:
                    # Create doctor info object
                    doctor_info = {
                        "name": full_name,
                        "email": email,
                        "phone": phone,
                        "specialization": specialization,
                        "experience": experience,
                        "license": license_number,
                        "hospital": hospital,
                        "username": username.lower(),
                        "password": sha256(password.encode()).hexdigest(),
                        "notes": notes,
                        "application_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "application_id": f"APP_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{username.lower()}"
                    }
                    
                    # Send email notification
                    if send_signup_email(doctor_info):
                        st.markdown('<div class="success-box-3d">', unsafe_allow_html=True)
                        st.markdown("### ✅ Application Submitted Successfully!")
                        st.markdown(f"**Application ID:** {doctor_info['application_id']}")
                        st.markdown("**Next Steps:**")
                        st.markdown("- Our team will review your application within 24-48 hours")
                        st.markdown("- You will receive an email notification with the decision")
                        st.markdown("- If approved, you'll receive login credentials")
                        st.markdown("- If you have any questions, please contact support")
                        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Back to login option - centered and separated
        st.markdown("<br><br>", unsafe_allow_html=True)
        col_back1, col_back2, col_back3 = st.columns([1, 2, 1])
        with col_back2:
            if st.button("🔙 Back to Login", key="signup_back_btn", use_container_width=True):
                st.session_state.show_signup = False
                st.rerun()
        
        st.markdown('<div style="text-align: center; margin-top: 20px;">', unsafe_allow_html=True)
        st.markdown("**Already have an account?** Use the button above to return to login.")
        st.markdown('</div>', unsafe_allow_html=True)
    

def dashboard_page():
    """Main dashboard"""
    doctor = st.session_state.current_doctor
    
    # Header with logout
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f'<h1 class="main-title">Welcome, {doctor["name"]}</h1>', unsafe_allow_html=True)
        st.markdown(f"**Specialization:** {doctor['specialization']}")
    with col2:
        if st.button("🚪 Logout", key="logout_btn"):
            st.session_state.logged_in = False
            st.session_state.current_doctor = None
            st.rerun()
    
    # Statistics dashboard
    st.markdown('<div class="card-3d">', unsafe_allow_html=True)
    st.markdown("### 📊 Today's Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👥 Total Patients", len(st.session_state.patients_data), "2")
    with col2:
        benign_count = sum(1 for p in st.session_state.patients_data.values() if p.get('diagnosis') == 'Benign')
        st.metric("✅ Benign Cases", benign_count, "1")
    with col3:
        malignant_count = sum(1 for p in st.session_state.patients_data.values() if p.get('diagnosis') == 'Malignant')
        st.metric("⚠️ Malignant Cases", malignant_count, "0")
    with col4:
        st.metric("🔬 Pending Tests", "3", "-1")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Recent patients
    if st.session_state.patients_data:
        st.markdown('<div class="card-3d">', unsafe_allow_html=True)
        st.markdown("### 👥 Recent Patients")
        
        for patient_id, patient_data in list(st.session_state.patients_data.items())[-5:]:
            st.markdown(f'<div class="patient-card">', unsafe_allow_html=True)
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.write(f"**{patient_data.get('name', 'Unknown')}**")
                st.write(f"ID: {patient_id}")
            with col2:
                diagnosis = patient_data.get('diagnosis', 'Pending')
                color = '🟢' if diagnosis == 'Benign' else '🔴' if diagnosis == 'Malignant' else '🟡'
                st.write(f"**Diagnosis:** {color} {diagnosis}")
                st.write(f"**Date:** {patient_data.get('date', 'N/A')}")
            with col3:
                if st.button(f"View", key=f"view_{patient_id}"):
                    st.session_state.selected_patient = patient_id
                    st.session_state.page = "Patient Details"
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def diagnosis_page():
    """Diagnosis analysis page"""
    st.markdown('<h2 class="main-title">🔬 Patient Diagnosis</h2>', unsafe_allow_html=True)
    
    # Patient Information Form
    st.markdown('<div class="card-3d">', unsafe_allow_html=True)
    st.markdown("### 👤 Patient Information")
    
    col1, col2 = st.columns(2)
    with col1:
        patient_name = st.text_input("📝 Patient Name", key="patient_name")
        patient_age = st.number_input("🎂 Age", min_value=0, max_value=120, key="patient_age")
    with col2:
        patient_id = st.text_input("🆔 Patient ID", key="patient_id")
        patient_gender = st.selectbox("⚧ Gender", ["Female", "Male", "Other"], key="patient_gender")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Medical Measurements
    st.markdown('<div class="card-3d">', unsafe_allow_html=True)
    st.markdown("### 🔬 Cell Nuclei Measurements")
    
    # Sample data
    if 'sample_loaded' not in st.session_state:
        st.session_state.sample_loaded = None
    
    benign_sample = [12.0, 14.0, 78.0, 450.0, 0.09, 0.08, 0.02, 0.02, 0.18, 0.06,
                    0.3, 0.9, 2.0, 24.0, 0.007, 0.02, 0.02, 0.01, 0.02, 0.003,
                    13.0, 16.0, 85.0, 520.0, 0.11, 0.13, 0.04, 0.04, 0.22, 0.07]
    
    malignant_sample = [18.0, 22.0, 120.0, 1000.0, 0.12, 0.25, 0.18, 0.09, 0.22, 0.08,
                       0.6, 1.2, 4.0, 80.0, 0.01, 0.05, 0.07, 0.03, 0.03, 0.005,
                       21.0, 28.0, 140.0, 1500.0, 0.15, 0.35, 0.25, 0.13, 0.30, 0.09]
    
    # Quick load buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧬 Load Benign Sample", key="load_benign"):
            st.session_state.sample_loaded = 'benign'
            st.rerun()
    with col2:
        if st.button("⚠️ Load Malignant Sample", key="load_malignant"):
            st.session_state.sample_loaded = 'malignant'
            st.rerun()
    
    # Input fields in three columns
    col1, col2, col3 = st.columns(3)
    inputs = []
    
    with col1:
        st.markdown("#### 📊 Mean Values")
        for i in range(0, 10):
            default_val = 0.0
            if st.session_state.sample_loaded == 'benign':
                default_val = benign_sample[i]
            elif st.session_state.sample_loaded == 'malignant':
                default_val = malignant_sample[i]
            
            value = st.number_input(f"{feature_names[i]}", min_value=0.0, format="%.4f", 
                                  key=f"mean_{i}", value=default_val)
            inputs.append(value)
    
    with col2:
        st.markdown("#### 📈 Standard Error")
        for i in range(10, 20):
            default_val = 0.0
            if st.session_state.sample_loaded == 'benign':
                default_val = benign_sample[i]
            elif st.session_state.sample_loaded == 'malignant':
                default_val = malignant_sample[i]
            
            value = st.number_input(f"{feature_names[i]}", min_value=0.0, format="%.4f", 
                                  key=f"se_{i}", value=default_val)
            inputs.append(value)
    
    with col3:
        st.markdown("#### 🔻 Worst Values")
        for i in range(20, 30):
            default_val = 0.0
            if st.session_state.sample_loaded == 'benign':
                default_val = benign_sample[i]
            elif st.session_state.sample_loaded == 'malignant':
                default_val = malignant_sample[i]
            
            value = st.number_input(f"{feature_names[i]}", min_value=0.0, format="%.4f", 
                                  key=f"worst_{i}", value=default_val)
            inputs.append(value)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Analysis Button
    if st.button("🔬 Run Diagnosis Analysis", key="analyze_btn"):
        if not patient_name or not patient_id:
            st.error("❌ Please fill in patient name and ID")
        elif all(x == 0.0 for x in inputs):
            st.warning("⚠️ Please enter measurement values")
        else:
            # Perform analysis
            input_array = np.array(inputs).reshape(1, -1)
            input_array_scaled = scaler.transform(input_array)
            
            prediction = model.predict(input_array_scaled)[0]
            proba = model.predict_proba(input_array_scaled)[0]
            confidence = np.max(proba) * 100
            
            diagnosis = "Benign" if prediction == 0 else "Malignant"
            
            # Save patient data
            patient_data = {
                'name': patient_name,
                'age': patient_age,
                'gender': patient_gender,
                'diagnosis': diagnosis,
                'prediction': diagnosis,  # alias for statistics module
                'confidence': confidence,
                'measurements': inputs,
                'features': {feature_names[i]: inputs[i] for i in range(len(feature_names))},
                'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                'doctor': st.session_state.current_doctor['name'],
                'proba': proba.tolist()
            }
            save_patient_data(patient_id, patient_data)
            
            # Display results
            if diagnosis == "Malignant":
                st.markdown(f'''
                <div class="warning-box-3d">
                    <h3>🚨 DIAGNOSIS: MALIGNANT</h3>
                    <h4>Confidence: {confidence:.2f}%</h4>
                    <p><strong>Patient:</strong> {patient_name} (ID: {patient_id})</p>
                    <p><strong>Analyzed by:</strong> {st.session_state.current_doctor["name"]}</p>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="success-box-3d">
                    <h3>✅ DIAGNOSIS: BENIGN</h3>
                    <h4>Confidence: {confidence:.2f}%</h4>
                    <p><strong>Patient:</strong> {patient_name} (ID: {patient_id})</p>
                    <p><strong>Analyzed by:</strong> {st.session_state.current_doctor["name"]}</p>
                </div>
                ''', unsafe_allow_html=True)
            
            st.success(f"✅ Patient data saved successfully!")

def patients_page():
    """Patient management page"""
    st.markdown('<h2 class="main-title">👥 Patient Management</h2>', unsafe_allow_html=True)
    
    if not st.session_state.patients_data:
        st.markdown('<div class="card-3d">', unsafe_allow_html=True)
        st.markdown("### 📋 No Patients Found")
        st.write("No patient records available. Start by running a diagnosis analysis.")
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # Patient list
    st.markdown('<div class="card-3d">', unsafe_allow_html=True)
    st.markdown("### 📋 All Patients")
    
    for patient_id, patient_data in st.session_state.patients_data.items():
        st.markdown('<div class="patient-card">', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
        with col1:
            st.write(f"**{patient_data.get('name', 'Unknown')}**")
            st.write(f"ID: {patient_id}")
            st.write(f"Age: {patient_data.get('age', 'N/A')}")
        
        with col2:
            diagnosis = patient_data.get('diagnosis', 'Pending')
            confidence = patient_data.get('confidence', 0)
            color = '🟢' if diagnosis == 'Benign' else '🔴'
            st.write(f"**Diagnosis:** {color} {diagnosis}")
            st.write(f"**Confidence:** {confidence:.1f}%")
        
        with col3:
            st.write(f"**Date:** {patient_data.get('date', 'N/A')}")
            st.write(f"**Doctor:** {patient_data.get('doctor', 'N/A')}")
        
        with col4:
            if st.button("📋 Details", key=f"details_{patient_id}"):
                st.session_state.selected_patient = patient_id
                st.session_state.page = "Patient Details"
                st.rerun()
            
            if st.button("🗑️ Delete", key=f"delete_{patient_id}"):
                del st.session_state.patients_data[patient_id]
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def patient_details_page():
    """Patient details and treatment plan page"""
    patient_id = st.session_state.get('selected_patient')
    if not patient_id or patient_id not in st.session_state.patients_data:
        st.error("❌ Patient not found")
        return
    
    patient_data = st.session_state.patients_data[patient_id]
    
    st.markdown('<h2 class="main-title">📋 Patient Details</h2>', unsafe_allow_html=True)
    
    # Patient Information
    st.markdown('<div class="card-3d">', unsafe_allow_html=True)
    st.markdown("### 👤 Patient Information")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Name:** {patient_data.get('name', 'Unknown')}")
        st.write(f"**ID:** {patient_id}")
        st.write(f"**Age:** {patient_data.get('age', 'N/A')}")
        st.write(f"**Gender:** {patient_data.get('gender', 'N/A')}")
    
    with col2:
        diagnosis = patient_data.get('diagnosis', 'Unknown')
        confidence = patient_data.get('confidence', 0)
        color = '🟢' if diagnosis == 'Benign' else '🔴'
        st.write(f"**Diagnosis:** {color} {diagnosis}")
        st.write(f"**Confidence:** {confidence:.2f}%")
        st.write(f"**Date:** {patient_data.get('date', 'N/A')}")
        st.write(f"**Analyzing Doctor:** {patient_data.get('doctor', 'N/A')}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Treatment Plan
    st.markdown('<div class="card-3d">', unsafe_allow_html=True)
    st.markdown("### 🏥 Treatment Plan")
    
    # Get or create treatment plan
    if 'treatment_plan' not in patient_data:
        patient_data['treatment_plan'] = ""
    
    treatment_plan = st.text_area(
        "Treatment Plan", 
        value=patient_data['treatment_plan'],
        height=200,
        placeholder="Enter treatment recommendations, follow-up schedule, medications, etc."
    )
    
    # Notes
    if 'notes' not in patient_data:
        patient_data['notes'] = ""
    
    notes = st.text_area(
        "Doctor's Notes", 
        value=patient_data['notes'],
        height=150,
        placeholder="Additional notes, observations, recommendations..."
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save Changes", key="save_changes"):
            patient_data['treatment_plan'] = treatment_plan
            patient_data['notes'] = notes
            st.session_state.patients_data[patient_id] = patient_data
            st.success("✅ Changes saved successfully!")
    
    with col2:
        if st.button("🔙 Back to Patients", key="back_to_patients"):
            st.session_state.page = "Patient Management"
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Probability Details
    if 'proba' in patient_data:
        st.markdown('<div class="card-3d">', unsafe_allow_html=True)
        st.markdown("### 📊 Analysis Details")
        
        proba = patient_data['proba']
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🟢 Benign Probability", f"{proba[0]*100:.2f}%")
        with col2:
            st.metric("🔴 Malignant Probability", f"{proba[1]*100:.2f}%")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Main App Logic
def main():
    """Main function to run the application"""
    # Process approval/rejection links via query params early
    # Using new st.query_params (dict-like) instead of deprecated experimental API
    qp = st.query_params
    app_id_param = qp.get('app_id')
    action_param = qp.get('action')
    token_param = qp.get('token')
    if app_id_param and action_param in ('accept','reject') and token_param:
        info = db_get_pending(app_id_param)
        if info and _verify_token(app_id_param, action_param, token_param):
            if action_param == 'accept':
                db_insert_doctor(info)
                accept_body = f"""
                <html><body>
                <h2>✅ Application Approved</h2>
                <p>Dear Dr. {info['name']},</p>
                <p>Your application (ID {info['application_id']}) has been <strong>approved</strong>. You can now log in using your chosen username <strong>{info['username']}</strong>.</p>
                <p>For security, we never send your password back. Use the password you created during signup.</p>
                <p><a href='{_get_base_url()}' style='background:#4caf50;color:#fff;padding:10px 16px;text-decoration:none;border-radius:6px;'>Log In Now</a></p>
                <hr><p style='font-size:12px;color:#666'>Medical Diagnosis System</p>
                </body></html>
                """
                send_generic_email(info['email'], '✅ Your Account Has Been Approved', accept_body)
                st.success(f"Application {app_id_param} approved and doctor account activated.")
            else:
                reject_body = f"""
                <html><body>
                <h2>❌ Application Update</h2>
                <p>Dear Dr. {info['name']},</p>
                <p>Your application (ID {info['application_id']}) was <strong>not approved</strong> at this time.</p>
                <p>If you believe this is an error you may reapply with updated information.</p>
                <hr><p style='font-size:12px;color:#666'>Medical Diagnosis System</p>
                </body></html>
                """
                send_generic_email(info['email'], '❌ Application Status Update', reject_body)
                st.warning(f"Application {app_id_param} rejected.")
            db_delete_pending(app_id_param)
            st.query_params.clear()
        elif info:
            st.error("Invalid or expired action link (token mismatch).")
        # else silently ignore if unknown app id
    # Initialize session states
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'show_signup' not in st.session_state:
        st.session_state.show_signup = False
    # pending_applications kept for backward compatibility; DB persists actual data
    if 'pending_applications' not in st.session_state:
        st.session_state.pending_applications = {}
    if 'current_doctor' not in st.session_state:
        st.session_state.current_doctor = None
    if 'patients_data' not in st.session_state:
        st.session_state.patients_data = {}
    if 'page' not in st.session_state:
        st.session_state.page = "Dashboard"
    
    # Check if user is logged in
    if not st.session_state.logged_in:
        if st.session_state.show_signup:
            signup_page()
        else:
            login_page()
    else:
        # Sidebar navigation
        with st.sidebar:
            st.markdown(f"### 👨‍⚕️ {st.session_state.current_doctor['name']}")
            st.markdown(f"**{st.session_state.current_doctor['specialization']}**")
            
            st.markdown("---")
            
            pages = {
                "🏠 Dashboard": "Dashboard",
                "🔬 New Diagnosis": "Diagnosis",
                "👥 Patient Management": "Patient Management",
                "📊 Statistics": "Statistics"
            }
            
            for page_name, page_key in pages.items():
                if st.button(page_name, key=f"nav_{page_key}"):
                    st.session_state.page = page_key
                    st.rerun()
            
            st.markdown("---")
            
            # Quick stats
            st.markdown("### 📈 Quick Stats")
            st.write(f"Total Patients: {len(st.session_state.patients_data)}")
            
            if st.button("🚪 Logout", key="sidebar_logout"):
                st.session_state.logged_in = False
                st.session_state.current_doctor = None
                st.session_state.show_signup = False
                st.rerun()
        
        # Main content
        if st.session_state.page == "Dashboard":
            dashboard_page()
        elif st.session_state.page == "Diagnosis":
            diagnosis_page()
        elif st.session_state.page == "Patient Management":
            patients_page()
        elif st.session_state.page == "Patient Details":
            patient_details_page()
        elif st.session_state.page == "Statistics":
            st.markdown('<h2 class="main-title">📊 Statistics</h2>', unsafe_allow_html=True)
            patients = st.session_state.patients_data
            total = len(patients)
            malignant = sum(1 for p in patients.values() if p.get('prediction') == 'Malignant')
            benign = sum(1 for p in patients.values() if p.get('prediction') == 'Benign')
            malignant_pct = (malignant/total*100) if total else 0
            benign_pct = (benign/total*100) if total else 0

            col_a, col_b, col_c, col_d = st.columns(4)
            with col_a:
                st.metric("Total Patients", total)
            with col_b:
                st.metric("Malignant Cases", malignant, f"{malignant_pct:.1f}%")
            with col_c:
                st.metric("Benign Cases", benign, f"{benign_pct:.1f}%")
            with col_d:
                st.metric("Doctors (DB)", _doctor_count())

            # ================== GLOBAL AGGREGATES ==================
            st.markdown("### 🌐 Global Trends")
            # Time-series (by date added)
            if total:
                import pandas as pd
                rows = []
                for pid, pdata in patients.items():
                    ts = pdata.get('timestamp') or pdata.get('created_at') or pid
                    pred_val = pdata.get('prediction')
                    if pred_val is None:
                        # Fallback to 'diagnosis' key if 'prediction' absent
                        pred_val = pdata.get('diagnosis')
                    rows.append({
                        'patient_id': pid,
                        'date': str(ts)[:10],
                        'prediction': pred_val
                    })
                df = pd.DataFrame(rows)
                with st.expander("📅 Cases Over Time", expanded=True):
                    by_date = df.groupby('date').size().reset_index(name='count')
                    st.bar_chart(by_date.set_index('date'))

                with st.expander("🔍 Prediction Distribution"):
                    # Drop rows with completely missing prediction
                    df_pred = df.dropna(subset=['prediction'])
                    if df_pred.empty:
                        st.info("No prediction data available yet.")
                    else:
                        dist = df_pred['prediction'].value_counts().reset_index()
                        dist.columns = ['prediction','count']
                        st.write(dist)
                        fig = _plot_pie(dist)
                        if fig:
                            st.pyplot(fig)

                # Feature summary if features stored
                feature_rows = []
                for pid, pdata in patients.items():
                    feats = pdata.get('features') or {}
                    if isinstance(feats, dict):
                        feature_rows.append({'patient_id': pid, **feats})
                if feature_rows:
                    fdf = pd.DataFrame(feature_rows)
                    with st.expander("🧬 Feature Averages (Top 10)"):
                        means = fdf.drop(columns=['patient_id']).mean().sort_values(ascending=False).head(10)
                        st.bar_chart(means)
            else:
                st.info("No patient data yet. Add diagnoses to see statistics.")

            # ================== PER-PATIENT DETAIL ==================
            st.markdown("### 👤 Patient-Specific Analytics")
            if patients:
                sel_id = st.selectbox("Select Patient", options=sorted(patients.keys()), key="stats_patient_select")
                p = patients.get(sel_id)
                if p:
                    colp1, colp2, colp3, colp4 = st.columns(4)
                    colp1.metric("Prediction", p.get('prediction','-'))
                    colp2.metric("Diagnosis", p.get('diagnosis','-'))
                    colp3.metric("Risk Score", f"{p.get('risk_score','-')}")
                    created = p.get('created_at') or p.get('timestamp','-')
                    colp4.metric("Created", str(created)[:19])

                    # Treatment progress tracking
                    if 'progress' not in p:
                        p['progress'] = []  # list of {date, note, status}
                    with st.expander("🩺 Treatment Plan & Progress", expanded=True):
                        current_plan = p.get('treatment_plan','')
                        new_plan = st.text_area("Treatment Plan (editable)", value=current_plan, key=f"plan_{sel_id}")
                        prog_col1, prog_col2 = st.columns([3,1])
                        with prog_col1:
                            new_progress_note = st.text_input("Add Progress Note", key=f"prog_note_{sel_id}")
                        with prog_col2:
                            status = st.selectbox("Status", ["Planned","Ongoing","Completed"], key=f"prog_status_{sel_id}")
                        if st.button("➕ Add Progress Entry", key=f"add_prog_{sel_id}") and new_progress_note:
                            p['progress'].append({
                                'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                                'note': new_progress_note,
                                'status': status
                            })
                            st.success("Progress entry added.")
                        if new_plan != current_plan:
                            p['treatment_plan'] = new_plan
                        # Display progress timeline
                        if p['progress']:
                            st.markdown("#### Timeline")
                            for entry in reversed(p['progress'][-25:]):
                                st.write(f"{entry['date']} - [{entry['status']}] {entry['note']}")
                        else:
                            st.info("No progress entries yet.")

                    # Simple feature radar / bar for this patient vs mean
                    feats = p.get('features')
                    if isinstance(feats, dict) and feature_rows:
                        try:
                            import pandas as pd, math
                            subset_cols = list(feats.keys())[:8]
                            patient_vals = [feats[c] for c in subset_cols]
                            # Compute mean across patients
                            fdf_use = fdf[subset_cols].mean()
                            comp_df = pd.DataFrame({
                                'feature': subset_cols,
                                'patient': patient_vals,
                                'average': [fdf_use[c] for c in subset_cols]
                            })
                            with st.expander("🧪 Feature Comparison (Patient vs Average)", expanded=False):
                                st.bar_chart(comp_df.set_index('feature'))
                        except Exception as e:
                            st.warning(f"Comparison unavailable: {e}")
            else:
                st.info("No patients to analyze.")

            with st.expander("⚙️ Data Quality Checks"):
                issues = []
                for pid, pdata in patients.items():
                    if 'prediction' not in pdata:
                        issues.append(f"Patient {pid} missing prediction")
                    if 'features' not in pdata:
                        issues.append(f"Patient {pid} missing raw features")
                if issues:
                    for i in issues[:25]:
                        st.warning(i)
                    if len(issues) > 25:
                        st.warning(f"... {len(issues)-25} more issues")
                else:
                    st.success("No data issues detected.")

if __name__ == "__main__":
    main()
