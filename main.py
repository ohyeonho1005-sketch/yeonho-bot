from keep_alive import keep_alive
import sys
import random
import string
import os
import shutil
import tempfile
import time
import hashlib
import platform
import subprocess
import json
import datetime
import re
import asyncio
import aiohttp
import base64

# PyQt6 Imports
from PyQt6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    QLabel, QTextEdit, QLineEdit, QProgressBar, QFrame,
    QGraphicsDropShadowEffect, QFileDialog, QComboBox, QTabWidget,
    QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox
)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, QPoint, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QPainter, QColor, QBrush, QImage, QPen, QFont, QPixmap, QPainterPath, QMovie

# Discord API Import
import discord

try:
    from aiohttp_socks import ProxyConnector
    SOCKS_AVAILABLE = True
except ImportError:
    SOCKS_AVAILABLE = False

import openai

# Firebase Admin SDK (Optional import fallback if not installed)
try:
    import firebase_admin
    from firebase_admin import credentials, db
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False

# ==============================================================================
# CONFIGURATIONS & CRITICAL CREDENTIALS
# ==============================================================================
DATABASE_URL = "https://hijn-aed32-default-rtdb.firebaseio.com/"
BYPASS_AUTH = True  # Set to True to allow offline verification using key format regex

FIREBASE_CONFIG = {
    "type": "service_account",
    "project_id": "hijn-aed32",
    "private_key_id": "bbcccf952e006952fbe81dc16e4f17eacd940af8",
    "private_key": (
        "-----BEGIN PRIVATE KEY-----\n"
        "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC6CqxmRUFyY/9x\n"
        "9zIu5Mn9SS1nm4MXfUJFHhc6QWbpP6Oa/9HvXb2NpAXPZPw0LOnb53ReaPTIUHXz\n"
        "AD2iHNIgaqeGpcuPq9pyZHsjtkXS1NQzlNoaDWSMLGf1remHwF8SJzELbm4k2otQ\n"
        "iFJaOd1WQNelwN2lvQqTg32MT42vnyG0Wpqbxc2s/AKBFbmznEepUTSU1PQS8blY\n"
        "FxX3C0jn6BA0xvEsqKr+LFewkhDFi+cA7+7WYN1MDRfIcHSPkFYyCoxo57BojhEG\n"
        "uSvGN9v4g7NI6yXxWDKq+YUsIrVrXu00XAUN5gkfiK7RQcVwPySde+dr+LRm/dUt\n"
        "oxyOd5ZrAgMBAAECggEASOQ0ru9UmKqYY8EsLtZiU7Rvr0ftgW8I34bOJ/uHBD10\n"
        "bx7rVKNASPYqdptE+3ZbfFb/r5vkyHVJ+VcvTsyHAb93+tgL3TNCqA45dwEL83KC\n"
        "3+Di4VE9A3TEmKw2swMK3NRxMV7nldXwvrFivsosMAbA10ctMKpUMf7TWn2y8Es3\n"
        "gBg8d0Tsjoh80YNyRQv8vJ5Q4C4MfMRkXrm/noN5j45ga4urku7zVvN43hECKdew\n"
        "V5AuD0xddnIo4Ii/QDWA6x/Y1sf2M8e80q8bJD6xsZNpH9WC9UL92VnPPIxB6oH6\n"
        "7m30Ve5xH4h7Ath0ZHCtSveFvk+Z+JD/owejSr2VaQKBgQDzlhhiwLg3fyFqEuB0\n"
        "oKaaoXLj/vBr9eVYmRQI2UqiUtew/TD+/R+29ld1w+dkT3mVQsGMQofpZm1Y7zwe\n"
        "JTczs3KgzftDCa1Sy+4+OZQMVgBtmPN8TEAyMk6Uz8erpQhhJzLDxIvRhGpEFXCt\n"
        "+SaSEqxCpocClkVQO0eNhGB/uQKBgQDDhdUuw12qe6r54CAlXDIFN7ulEd4+em1H\n"
        "N52ZlBA9MOcd+G5W+Xp24WUSpECNefx2sENa+IS5oBF/dqGxkywLg0bPra3DGUJf\n"
        "GnnqOI+h/YQoVCyI4aBCG/Y4Wq+MNlR/tvQJ2bpBhCRwMaFkyD6f+aHo9N36nP4g\n"
        "ZpukO0HxQwKBgEgfwDa1U5ZzGSS8VCOUUeBlP4yMtwlwdKkoIkuAc13e46ivP2uw\n"
        "7UwSYtEm4YPNGHX+nyp1pKKSRnxX0dgnMtInJyC//M7btatXYMKh79k7OcM5z5aV\n"
        "SUjTpnrfjwKeyf1iSuC2eKPf7kscghGxPR9xUfomLsGwVvOrqcMYWC5ZAoGAO57D\n"
        "ss6/8Qxkxm0hYEMMvaqQ/XTFYCfUyrKazAnqKb6PuwPWIY9RWI7CUzziskFQSqDU\n"
        "6Rh+4Ft++m8iPxOxipEtNoavRZ6eLoHUSyeUJME5W1LPga3LQF1mZyi//vFSMt+G\n"
        "6roJoZC5y7xWinTFI+LrDC4ewhy9IQQo0ZuAMCECgYEA689he3SaoFVXoOfTLKyp\n"
        "M4m2e1vs3uJ7SFbwO/6rRaS6UdOOh68MsKbvkOTtnBaH06RL57a0xAAibJdRKgEW\n"
        "/qAnHHQ0ajiTYMDl3HjNxFWBV/urRCf/+WVh0/SvbQUay0EVHjBHkdC6UfWfKYQT\n"
        "nk6jpqTpci9DvQuVoEIqMkc=\n"
        "-----END PRIVATE KEY-----\n"
    ),
    "client_email": "firebase-adminsdk-fbsvc@hijn-aed32.iam.gserviceaccount.com",
    "client_id": "111960002056714376759",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40hijn-aed32.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

# Initialize Firebase Admin SDK
db_ref = None
if FIREBASE_AVAILABLE:
    try:
        cred = credentials.Certificate(FIREBASE_CONFIG)
        firebase_admin.initialize_app(cred, {"databaseURL": DATABASE_URL})
        db_ref = db.reference()
    except Exception as e:
        print(f"Firebase 초기화 실패: {e}")

# ==============================================================================
# ANTI-DETECTION: DISCORD CLIENT DISGUISE
# ==============================================================================
DISCORD_SUPER_PROPERTIES = base64.b64encode(json.dumps({
    "os": "Windows",
    "browser": "Discord Client",
    "release_channel": "stable",
    "client_version": "1.0.9163",
    "os_version": "10.0.22631",
    "os_arch": "x64",
    "app_arch": "x64",
    "system_locale": "ko",
    "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9163 Chrome/124.0.6367.243 Electron/30.2.0 Safari/537.36",
    "browser_version": "30.2.0",
    "client_build_number": 318966,
    "native_build_number": 54689,
    "client_event_source": None
}, separators=(',', ':')).encode()).decode()

def get_discord_headers(token):
    return {
        "Authorization": token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9163 Chrome/124.0.6367.243 Electron/30.2.0 Safari/537.36",
        "X-Super-Properties": DISCORD_SUPER_PROPERTIES,
        "X-Discord-Locale": "ko",
        "X-Discord-Timezone": "Asia/Seoul",
        "X-Debug-Options": "bugReporterEnabled",
        "Accept": "*/*",
        "Accept-Language": "ko-KR",
        "Sec-Ch-Ua": '"Chromium";v="124", "Not-A.Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
    }

# ==============================================================================
# PROXY MANAGER
# ==============================================================================
class ProxyManager:
    def __init__(self, filepath="settings/proxies.txt", log_callback=None):
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
        except NameError:
            base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        self.filepath = os.path.join(base_path, filepath)
        self.proxies = []
        self.index = 0
        self.log_callback = log_callback or print
        self.load_proxies()

    def log(self, text):
        self.log_callback(f"[Proxy] {text}")

    def load_proxies(self):
        self.proxies = []
        if not os.path.exists(self.filepath):
            self.log("⚠️ proxies.txt 파일이 없습니다. 직접 연결 모드로 작동합니다.")
            return
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    proxy = self._normalize_proxy(line)
                    if proxy:
                        self.proxies.append(proxy)
            self.index = 0
            if self.proxies:
                self.log(f"🔄 프록시 {len(self.proxies)}개 로드됨")
            else:
                self.log("⚠️ proxies.txt에 유효한 프록시가 없습니다. 직접 연결 모드로 작동합니다.")
        except Exception as e:
            self.log(f"❌ proxies.txt 로드 실패: {e}")

    def _normalize_proxy(self, raw):
        raw = raw.strip()
        if raw.startswith("socks5://") or raw.startswith("socks4://"):
            return raw
        if raw.startswith("http://") or raw.startswith("https://"):
            return raw
        if "@" in raw:
            return f"http://{raw}"
        if ":" in raw:
            return f"http://{raw}"
        return None

    def get_next(self):
        if not self.proxies:
            return None
        proxy = self.proxies[self.index % len(self.proxies)]
        self.index = (self.index + 1) % max(len(self.proxies), 1)
        return proxy

    def remove_proxy(self, proxy):
        if proxy in self.proxies:
            self.proxies.remove(proxy)
            self._save_to_file()
            masked = self._mask_proxy(proxy)
            self.log(f"❌ 죽은 프록시 제거됨: {masked} (남은: {len(self.proxies)}개)")
            if not self.proxies:
                self.log("⚠️ 모든 프록시 소진! 직접 연결 모드로 전환합니다.")

    def _mask_proxy(self, proxy):
        try:
            if "@" in proxy:
                parts = proxy.split("@")
                return f"***@{parts[-1]}"
            return proxy.split("//")[-1] if "//" in proxy else proxy
        except:
            return "***"

    def _save_to_file(self):
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                for p in self.proxies:
                    f.write(p + "\n")
        except Exception as e:
            self.log(f"❌ proxies.txt 저장 실패: {e}")

    async def check_proxy(self, proxy):
        try:
            timeout = aiohttp.ClientTimeout(total=8)
            if proxy.startswith("socks") and SOCKS_AVAILABLE:
                connector = ProxyConnector.from_url(proxy)
                async with aiohttp.ClientSession(connector=connector) as session:
                    async with session.get("https://discord.com/api/v9/gateway", timeout=timeout) as r:
                        return r.status == 200
            elif proxy.startswith("socks") and not SOCKS_AVAILABLE:
                return True
            else:
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://discord.com/api/v9/gateway", proxy=proxy, timeout=timeout) as r:
                        return r.status == 200
        except:
            return False

    async def check_all(self):
        alive, dead = 0, 0
        dead_list = []
        for proxy in list(self.proxies):
            is_alive = await self.check_proxy(proxy)
            if is_alive:
                alive += 1
            else:
                dead += 1
                dead_list.append(proxy)
            await asyncio.sleep(0.5)
        for proxy in dead_list:
            self.remove_proxy(proxy)
        return alive, dead

    def reload(self):
        self.load_proxies()

    def get_count(self):
        return len(self.proxies)

    def get_list_display(self):
        return [self._mask_proxy(p) for p in self.proxies]


# ==============================================================================
# DISCORD SESSION WITH DISGUISE + PROXY
# ==============================================================================
class DiscordSession:
    def __init__(self, token, proxy_manager=None):
        self.token = token
        self.proxy_manager = proxy_manager
        self.headers = get_discord_headers(token)
        self.proxy_url = proxy_manager.get_next() if proxy_manager else None
        self.session = None
        self.connector = None
        self._http_proxy = None

    async def __aenter__(self):
        if self.proxy_url and self.proxy_url.startswith("socks") and SOCKS_AVAILABLE:
            self.connector = ProxyConnector.from_url(self.proxy_url)
            self._http_proxy = None
        else:
            self._http_proxy = self.proxy_url
            self.connector = None
        self.session = aiohttp.ClientSession(
            headers=self.headers,
            connector=self.connector,
            timeout=aiohttp.ClientTimeout(total=15)
        )
        return self

    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()

    def get(self, url, **kwargs):
        if self._http_proxy:
            kwargs.setdefault('proxy', self._http_proxy)
        return self.session.get(url, **kwargs)

    def post(self, url, **kwargs):
        if self._http_proxy:
            kwargs.setdefault('proxy', self._http_proxy)
        return self.session.post(url, **kwargs)

    def put(self, url, **kwargs):
        if self._http_proxy:
            kwargs.setdefault('proxy', self._http_proxy)
        return self.session.put(url, **kwargs)

    def delete(self, url, **kwargs):
        if self._http_proxy:
            kwargs.setdefault('proxy', self._http_proxy)
        return self.session.delete(url, **kwargs)

    def patch(self, url, **kwargs):
        if self._http_proxy:
            kwargs.setdefault('proxy', self._http_proxy)
        return self.session.patch(url, **kwargs)

    async def handle_failure(self, proxy_to_check):
        if proxy_to_check and self.proxy_manager:
            is_alive = await self.proxy_manager.check_proxy(proxy_to_check)
            if not is_alive:
                self.proxy_manager.remove_proxy(proxy_to_check)

# ==============================================================================
# DISCORD SELFBOT CLIENT IMPLEMENTATION
# ==============================================================================
class SelfBot(discord.Client):
    def __init__(self, log_callback, config_data, proxy_manager=None):
        super().__init__()
        self.log_callback = log_callback
        self.config = config_data
        self.proxy_manager = proxy_manager or ProxyManager(log_callback=log_callback)

        self.prefix = self.config.get("prefix", "!")
        self.start_time = time.time()

        # Flags & States
        self.sniper_active = False
        self.spam_active = False
        self.rpc_active = False

        self.auto_message = None
        self.auto_message_active = False

        self.mimic_target = None
        self.mimic_active = False

        self.auto_emoji = None
        self.auto_emoji_target = None
        self.auto_emoji_active = False

        self.promo_message = None
        self.promo_tasks = {}

        self.rpc_data = {
            "title": "파편 셀프봇",
            "subtitle": "Running",
            "image": "",
            "button1_label": "Button 1",
            "button2_label": "Button 2",
            "button1_url": "https://github.com",
            "button2_url": "https://github.com",
        }

        # Anti-detection: Rate limiting & cooldowns
        self._last_cmd_time = 0
        self._cmd_cooldown = 1.5  # seconds between commands
        self._auto_reply_cooldown = {}  # channel_id -> last_reply_time
        self._passive_cooldown_sec = 2.5  # seconds between auto-replies per channel

    def log(self, text):
        self.log_callback(f"[Bot] {text}")

    async def safe_send(self, channel, content, skip_typing=False):
        """Send message with human-like typing simulation and rate limit handling"""
        try:
            if not skip_typing:
                async with channel.typing():
                    await asyncio.sleep(random.uniform(0.5, 1.5))
            else:
                await asyncio.sleep(random.uniform(0.3, 0.8))
            await channel.send(content)
        except discord.HTTPException as e:
            if e.status == 429:
                retry_after = getattr(e, 'retry_after', 3)
                self.log(f"⏳ Rate limit 감지, {retry_after:.1f}초 대기...")
                await asyncio.sleep(retry_after + random.uniform(0.5, 1.5))
                await channel.send(content)
            else:
                raise

    def _check_cmd_cooldown(self):
        """Check if enough time has passed since last command. Returns True if OK."""
        now = time.time()
        if now - self._last_cmd_time < self._cmd_cooldown:
            return False
        self._last_cmd_time = now
        return True

    def _check_passive_cooldown(self, channel_id):
        """Check passive feature cooldown per channel. Returns True if OK."""
        now = time.time()
        last = self._auto_reply_cooldown.get(channel_id, 0)
        if now - last < self._passive_cooldown_sec:
            return False
        self._auto_reply_cooldown[channel_id] = now
        return True

    async def on_ready(self):
        self.log(f"🟢 로그인 성공: {self.user} ({self.user.id})")
        self.log(f"⚡ 접두사(Prefix): {self.prefix}")
        self.log(f"🔄 프록시: {self.proxy_manager.get_count()}개 로드됨")

    async def _promo_loop(self, channel, minutes):
        while True:
            try:
                if self.promo_message:
                    await self.safe_send(channel, self.promo_message)
                else:
                    break
            except Exception as e:
                self.log(f"홍보 전송 에러 ({channel.id}): {e}")
            await asyncio.sleep(minutes * 60)

    def _stop_promo(self, channel_id):
        if channel_id in self.promo_tasks:
            self.promo_tasks[channel_id].cancel()
            del self.promo_tasks[channel_id]

    async def on_message(self, message):
        # Passive features (triggered by other users)
        if message.author.id != self.user.id:
            if self.auto_message_active and self.auto_message:
                if self.user.mentioned_in(message) and not message.mention_everyone:
                    if self._check_passive_cooldown(message.channel.id):
                        try:
                            await asyncio.sleep(random.uniform(0.1, 0.5))
                            await self.safe_send(message.channel, self.auto_message)
                            self.log(f"자동 응답 전송 완료 -> {message.author}")
                        except Exception as e:
                            self.log(f"자동 응답 전송 실패: {e}")

            if self.mimic_active and self.mimic_target:
                if message.author.id == self.mimic_target:
                    try:
                        await asyncio.sleep(random.uniform(0.1, 0.5))
                        await self.safe_send(message.channel, message.content)
                        self.log(f"따라하기(Mimic) 전송 완료 -> {message.author}: {message.content}")
                    except Exception as e:
                        self.log(f"따라하기 전송 실패: {e}")

            if self.auto_emoji_active and self.auto_emoji_target and self.auto_emoji:
                if message.author.id == self.auto_emoji_target:
                    if self._check_passive_cooldown(message.channel.id):
                        try:
                            await asyncio.sleep(random.uniform(1, 4))
                            await message.add_reaction(self.auto_emoji)
                            self.log(f"자동 이모지 반응 완료 -> {message.author}")
                        except Exception as e:
                            self.log(f"자동 이모지 반응 실패: {e}")
            return

        # Own messages → command dispatch
        content = message.content
        is_cmd = content.startswith(self.prefix)
        is_no_prefix_copy = content.startswith("서버복사")

        if not is_cmd and not is_no_prefix_copy:
            return

        if not self._check_cmd_cooldown():
            return  # Cooldown active, ignore command

        args = content.split()
        if is_no_prefix_copy:
            cmd = "서버복사"
        else:
            cmd = args[0].lower()
        p = self.prefix
        
        self.log(f"명령어 감지: {content}")
        # ══════════════════════════════════════════════════
        #  HELP MENUS
        # ══════════════════════════════════════════════════

        if cmd == f"{p}명령어":
            await message.channel.send(
                "```🚀 파편 셀봇 기능 🚀\n\n"
                "{🔥} !유틸리티\n"
                "{📰} !정보\n"
                "{🤖} !매크로\n"
                "{✨} !서버관리\n"
                "{🧨} !레이드\n"
                "{📩} !홍보\n"
                "{🪩} !rpc\n"
                "{🔄} !프록시```"
            )

        elif cmd == f"{p}유틸리티":
            await message.channel.send(
                "```⚡ 파편 셀프봇 !유틸리티 리스트 ⚡\n\n"
                "{⚡} !니트로 - 가짜니트로 링크 생성\n"
                "{⚡} !서버복사 <복사할서버id> <붙여넣을서버id> - 서버를 복사합니다\n"
                "{⚡} !ltc환율 <한국돈> - 한국돈을 ltc 가격으로 보여줍니다\n"
                "{⚡} !유로환율 <한국돈> - 한국돈을 유로 가격으로 보여줍니다\n"
                "{⚡} !달러환율 <한국돈> - 한국돈을 달러 가격으로 보여줍니다\n"
                "{⚡} !ctl환율 <ltc> - ltc를 한국돈으로 보여줍니다\n"
                "{⚡} !로유환율 <유로> - 유로를 한국돈으로 보여줍니다\n"
                "{⚡} !러달환율 <달러> - 달러를 한국돈으로 보여줍니다\n"
                "{⚡} !계좌설정 <계좌> - 계좌 명령어 사용시 나올 말 세팅\n"
                "{⚡} !계좌 - 계좌설정에서 세팅한 계좌가 나옴\n"
                "{⚡} !검색 <검색어> - 구글에 검색한 결과가 나옴\n"
                "{⚡} !해킹 <맨션> - 가짜이멜, ip, 전번을 랜덤으로 나오게하는 시뮬레이션\n"
                "{⚡} !사랑 <맨션1> <맨션2> - 맨션한 사람들이 서로 얼마나 사랑하는지 %로 나타냅니다.\n"
                "{⚡} !exit - 모든 서버 나가기\n"
                "{⚡} 서버복사 <복사할서버 id> <붙여넣을서버 id> - 서버를 복사합니다 (서버에 참가해있어야합니다)\n"
                "{⚡} !가동시간 - 셀프봇 가동시간 확인\n"
                "{⚡} !봇핑 - 셀프봇 핑 확인```"
            )

        elif cmd == f"{p}정보":
            await message.channel.send(
                "```📰 파편 셀프봇 !정보 리스트 📰\n\n"
                "{📰} !서버정보 <id> - 서버의 정보 출력\n"
                "{📰} !유저정보 <@맨션> 유저의 정보 출력\n"
                "{📰} !프사 <@맨션> - 유저의 프사 출력\n"
                "{📰} !배너 <@맨션> - 유저의 배너 출력\n"
                "{📰} !토큰조회 <토큰> - 토큰 정보 출력\n"
                "{📰} !ip [ip] - ip 정보 출력```"
            )

        elif cmd == f"{p}매크로":
            await message.channel.send(
                "```🤖 파편 셀프봇 !매크로 리스트 🤖\n\n"
                "{🤖} !도배 <횟수> <문구> - 횟수만큼 문구를 도배 (1~100 최대)\n"
                "{🤖} !도배중지 - 모든 도배 중지\n"
                "{🤖} !자동메세지 <메시지> - 누군가 맨션할때마다 설정된 메시지로 자동 답변\n"
                "{🤖} !자동메세지종료 - 자동메시지 종료\n"
                "{🤖} !mimic <@맨션> - 맨션한 상대의 채팅 따라하기\n"
                "{🤖} !stopmimic - mimic 중지\n"
                "{🤖} !자동이모지반응 <이모지> <@맨션> - 맨션한 유저에게 설정한 이모지 자동 반응\n"
                "{🤖} !자동이모지종료 - 자동이모지 종료```"
            )

        elif cmd == f"{p}서버관리":
            await message.channel.send(
                "```✨ 파편 셀프봇 !서버관리 리스트 ✨\n\n"
                "{✨} !탐아 <@맨션> <시간> <사유> - 설정한 시간만큼 유저를 타임아웃 후 dm으로 사유 전송\n"
                "{✨} !탐아해제 <@맨션> <사유> - 맨션한 유저 타임아웃 해제 후 dm으로 사유 전송\n"
                "{✨} !추방 <@맨션> <사유> - 맨션한 유저 서버추방 후 dm으로 사유 전송\n"
                "{✨} !차단 <@맨션> <사유> - 맨션한 유저 서버차단 후 dm으로 사유 전송\n"
                "{✨} !전체청소 <갯수> - 갯수만큼 모든 채팅 삭제 (1~100)\n"
                "{✨} !개인청소 <갯수> - 갯수만큼 개인 채팅 삭제 (1~100)\n"
                "{✨} !역할 <맨션> <역할id> - 맨션한 상대에게 설정한 역할id를 줍니다\n"
                "{✨} !역할롤 <역할id> - 서버의 모든 사람들에게 설정한 역할id를 줍니다```"
            )

        elif cmd == f"{p}rpc":
            await message.channel.send(
                "```🚀 파편 셀프봇 !rpc 리스트 🚀\n\n"
                "{🪩} !rpc시작 - rpc 시작 (활성화)\n"
                "{🪩} !rpc종료 - rpc 종료 (비활성화)\n"
                "{🪩} !제목 <문구> - rpc 제목 변경\n"
                "{🪩} !부제목 <문구> - rpc 부제목 변경 (작은 글씨)\n"
                "{🪩} !사진변경 <url> - rpc 사진변경\n"
                "{🪩} !링크변경 <링크1> <링크2> - 박스에 들어갈 링크\n"
                "{🪩} !박스이름변경 <이름1> <이름2> - rpc 박스 이름 변경```"
            )

        elif cmd == f"{p}홍보":
            await message.channel.send(
                "```🚀 파편 셀프봇 !홍보 리스트 🚀\n\n"
                "{📩} !홍보문구 <문구> - 홍보 문구 저장\n"
                "{📩} !홍보시작 <분> - 설정한 시간만큼 해당 채널에 문구 전송\n"
                "{📩} !홍보중지 - 현재 채널의 홍보 루프 중지\n"
                "{📩} !홍보목록 - 홍보문구와 !홍보시작으로 저장된 채널들 id```"
            )

        elif cmd == f"{p}레이드":
            await message.channel.send(
                "```🧨 파편 셀프봇 !레이드 리스트 🧨\n\n"
                "⚠️ 레이드 기능은 보안 정책에 따라 현재 비활성화 상태입니다.```"
            )

        elif cmd == f"{p}프록시":
            await message.channel.send(
                "```🔄 파편 셀프봇 !프록시 리스트 🔄\n\n"
                "{🔄} !프록시목록 - 현재 로드된 프록시 목록 확인\n"
                "{🔄} !프록시체크 - 전체 프록시 상태 체크 (죽은 프록시 자동 삭제)\n"
                "{🔄} !프록시리로드 - settings/proxies.txt에서 프록시 다시 불러오기```"
            )

        # ══════════════════════════════════════════════════
        #  UTILITY
        # ══════════════════════════════════════════════════

        elif cmd == f"{p}니트로":
            code = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            await message.channel.send(f"🎁 https://discord.gift/{code}")

        elif cmd == f"{p}서버복사" or cmd == "서버복사":
            if len(args) < 3:
                await message.channel.send("사용법: !서버복사 <복사할서버id> <붙여넣을서버id>"); return
            src = self.get_guild(int(args[1]))
            dst = self.get_guild(int(args[2]))
            if not src or not dst:
                await message.channel.send("❌ 서버를 찾을 수 없습니다."); return
            copied = 0
            max_items = 20
            for ch in src.text_channels[:max_items]:
                try:
                    await dst.create_text_channel(
                        name=ch.name, topic=ch.topic,
                        slowmode_delay=ch.slowmode_delay, nsfw=ch.is_nsfw()
                    )
                    copied += 1
                    await asyncio.sleep(random.uniform(3.0, 6.0))
                except: pass
            role_count = 0
            for role in src.roles[:max_items]:
                if role.name == "@everyone": continue
                try:
                    await dst.create_role(
                        name=role.name, colour=role.colour,
                        permissions=role.permissions,
                        hoist=role.hoist, mentionable=role.mentionable
                    )
                    role_count += 1
                    await asyncio.sleep(random.uniform(3.0, 6.0))
                except: pass
            await message.channel.send(f"✅ 서버 복사 완료! 채널 {copied}개, 역할 {role_count}개 복사됨.")

        elif cmd == f"{p}ltc환율":
            if len(args) < 2:
                await message.channel.send("사용법: !ltc환율 <한국돈>"); return
            krw = float(args[1].replace(",", ""))
            async with aiohttp.ClientSession() as s:
                async with s.get("https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=krw") as r:
                    data = await r.json()
                    result = krw / data["litecoin"]["krw"]
                    await message.channel.send(f"💰 {krw:,.0f}원 = **{result:.6f} LTC**")

        elif cmd == f"{p}유로환율":
            if len(args) < 2:
                await message.channel.send("사용법: !유로환율 <한국돈>"); return
            krw = float(args[1].replace(",", ""))
            async with aiohttp.ClientSession() as s:
                async with s.get("https://api.exchangerate-api.com/v4/latest/KRW") as r:
                    data = await r.json()
                    await message.channel.send(f"💶 {krw:,.0f}원 = **{krw * data['rates']['EUR']:.2f} EUR**")

        elif cmd == f"{p}달러환율":
            if len(args) < 2:
                await message.channel.send("사용법: !달러환율 <한국돈>"); return
            krw = float(args[1].replace(",", ""))
            async with aiohttp.ClientSession() as s:
                async with s.get("https://api.exchangerate-api.com/v4/latest/KRW") as r:
                    data = await r.json()
                    await message.channel.send(f"💵 {krw:,.0f}원 = **{krw * data['rates']['USD']:.2f} USD**")

        elif cmd == f"{p}ctl환율":
            amount = 1.0
            if len(args) > 1:
                try: amount = float(args[1].replace(",", ""))
                except: pass
            async with aiohttp.ClientSession() as s:
                async with s.get("https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=krw") as r:
                    data = await r.json()
                    price = data['litecoin']['krw']
                    await message.channel.send(f"💰 {amount} LTC = **{price * amount:,.0f}원**")

        elif cmd == f"{p}로유환율":
            if len(args) < 2:
                await message.channel.send("사용법: !로유환율 <유로>"); return
            eur = float(args[1].replace(",", ""))
            async with aiohttp.ClientSession() as s:
                async with s.get("https://api.exchangerate-api.com/v4/latest/EUR") as r:
                    data = await r.json()
                    await message.channel.send(f"💶 {eur:.2f} EUR = **{eur * data['rates']['KRW']:,.0f}원**")

        elif cmd == f"{p}러달환율":
            if len(args) < 2:
                await message.channel.send("사용법: !러달환율 <달러>"); return
            usd = float(args[1].replace(",", ""))
            async with aiohttp.ClientSession() as s:
                async with s.get("https://api.exchangerate-api.com/v4/latest/USD") as r:
                    data = await r.json()
                    await message.channel.send(f"💵 {usd:.2f} USD = **{usd * data['rates']['KRW']:,.0f}원**")

        elif cmd == f"{p}계좌설정":
            if len(args) < 2:
                await message.channel.send("사용법: !계좌설정 <계좌>"); return
            self.config["account"] = " ".join(args[1:])
            try:
                with open("settings/config.json", "w", encoding="utf-8") as f:
                    json.dump(self.config, f, ensure_ascii=False, indent=4)
            except Exception as e:
                self.log(f"config.json 계좌 저장 실패: {e}")
            await message.channel.send(f"✅ 계좌 설정 완료: `{self.config['account']}`")

        elif cmd == f"{p}계좌":
            acc = self.config.get("account", "")
            if not acc:
                await message.channel.send("❌ 계좌가 설정되어 있지 않습니다.")
            else:
                await message.channel.send(f"💳 {acc}")

        elif cmd == f"{p}검색":
            if len(args) < 2:
                await message.channel.send("사용법: !검색 <검색어>"); return
            q = "+".join(args[1:])
            await message.channel.send(f"🔍 https://www.google.com/search?q={q}")

        elif cmd == f"{p}해킹":
            if not message.mentions:
                await message.channel.send("사용법: !해킹 <맨션>"); return
            t = message.mentions[0]
            email = ''.join(random.choices(string.ascii_lowercase, k=8)) + "@" + \
                    random.choice(["gmail.com","naver.com","yahoo.com","outlook.com"])
            ip    = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"
            phone = f"010-{random.randint(1000,9999)}-{random.randint(1000,9999)}"
            await message.channel.send(
                f"```\n🔓 해킹 시뮬레이션 - {t.name}\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"📧 이메일: {email}\n"
                f"🌐 IP주소: {ip}\n"
                f"📱 전화번호: {phone}\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"⚠️ [시뮬레이션입니다]\n```"
            )

        elif cmd == f"{p}사랑":
            if len(message.mentions) < 2:
                await message.channel.send("사용법: !사랑 <맨션1> <맨션2>"); return
            u1, u2 = message.mentions[0], message.mentions[1]
            pct = max((u1.id + u2.id) % 100, 15)
            bar = "❤️" * (pct // 10) + "🖤" * (10 - pct // 10)
            await message.channel.send(
                f"💘 **{u1.display_name}** 💕 **{u2.display_name}**\n{bar}\n**사랑 지수: {pct}%**"
            )

        elif cmd == f"{p}exit":
            await message.channel.send("👋 모든 서버에서 나갑니다...")
            for guild in self.guilds:
                try:
                    await guild.leave()
                    await asyncio.sleep(0.5)
                except: pass

        elif cmd == f"{p}가동시간":
            e = int(time.time() - self.start_time)
            await message.channel.send(f"⏱️ 가동시간: **{e//3600}시간 {(e%3600)//60}분 {e%60}초**")

        elif cmd == f"{p}봇핑":
            await message.channel.send(f"🏓 핑: **{round(self.latency * 1000)}ms**")
        # ══════════════════════════════════════════════════
        #  INFO
        # ══════════════════════════════════════════════════

        elif cmd == f"{p}서버정보":
            if len(args) < 2:
                await message.channel.send("사용법: !서버정보 <서버id>"); return
            try: gid = int(args[1])
            except:
                await message.channel.send("❌ 올바른 서버 ID를 입력해주세요."); return
            guild = self.get_guild(gid)
            if guild:
                bots   = sum(1 for m in guild.members if m.bot)
                humans = guild.member_count - bots
                online = sum(1 for m in guild.members if str(m.status) != 'offline')
                offline = guild.member_count - online
                percent = (online / guild.member_count * 100) if guild.member_count > 0 else 0
                await message.channel.send(
                    f"```\n🏠 서버 정보\n━━━━━━━━━━━━━━━━━━━━\n"
                    f"이름: {guild.name}\nID: {guild.id}\n"
                    f"오너: {guild.owner}\n설명: {guild.description or 'N/A'}\n"
                    f"멤버 수: {guild.member_count}명 (온라인: {online}명 | 오프라인: {offline}명)\n"
                    f"  └ 온라인율: {percent:.1f}%\n"
                    f"  └ 유저: {humans}명 | 봇: {bots}개\n"
                    f"채널 수: {len(guild.channels)}\n"
                    f"  └ 텍스트: {len(guild.text_channels)} | 음성: {len(guild.voice_channels)}\n"
                    f"역할 수: {len(guild.roles)}\n이모지 수: {len(guild.emojis)}\n"
                    f"부스트 레벨: {guild.premium_tier}\n부스트 수: {guild.premium_subscription_count}\n"
                    f"검증 레벨: {guild.verification_level}\n"
                    f"생성일: {guild.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"기능: {', '.join(guild.features) or 'N/A'}\n━━━━━━━━━━━━━━━━━━━━\n```"
                )
            else:
                async with DiscordSession(self.config["token"], self.proxy_manager) as s:
                    async with s.get(
                        f"https://discord.com/api/v9/guilds/{gid}?with_counts=true"
                    ) as r:
                        if r.status != 200:
                            await message.channel.send("❌ 서버를 찾을 수 없습니다."); return
                        d = await r.json()
                        total = d.get('approximate_member_count', 0)
                        online = d.get('approximate_presence_count', 0)
                        offline = total - online
                        percent = (online / total * 100) if total > 0 else 0
                        await message.channel.send(
                            f"```\n🏠 서버 정보\n━━━━━━━━━━━━━━━━━━━━\n"
                            f"이름: {d.get('name','N/A')}\nID: {d.get('id','N/A')}\n"
                            f"설명: {d.get('description') or 'N/A'}\n"
                            f"멤버 수: {total}명 (온라인: {online}명 | 오프라인: {offline}명)\n"
                            f"  └ 온라인율: {percent:.1f}%\n"
                            f"부스트 레벨: {d.get('premium_tier','N/A')}\n"
                            f"부스트 수: {d.get('premium_subscription_count','N/A')}\n"
                            f"검증 레벨: {d.get('verification_level','N/A')}\n"
                            f"기능: {', '.join(d.get('features',[])) or 'N/A'}\n"
                            f"━━━━━━━━━━━━━━━━━━━━\n```"
                        )

        elif cmd == f"{p}유저정보":
            if not message.mentions:
                await message.channel.send("사용법: !유저정보 <@맨션>"); return
            user = message.mentions[0]
            try:
                profile = await self.http.get_user_profile(
                    user.id,
                    with_mutual_guilds=False,
                    with_mutual_friends_count=False
                )
                member = message.guild.get_member(user.id) if message.guild else None
                flags  = user.public_flags
                badges = []
                if flags.staff:                   badges.append("Discord Staff")
                if flags.partner:                 badges.append("Partnered Owner")
                if flags.hypesquad:               badges.append("HypeSquad Events")
                if flags.bug_hunter:              badges.append("Bug Hunter")
                if flags.hypesquad_bravery:       badges.append("Bravery")
                if flags.hypesquad_brilliance:    badges.append("Brilliance")
                if flags.hypesquad_balance:       badges.append("Balance")
                if flags.early_supporter:         badges.append("Early Supporter")
                if flags.verified_bot_developer:  badges.append("Verified Bot Dev")
                if flags.active_developer:        badges.append("Active Developer")
                bio   = profile.get("user", {}).get("bio", "N/A") if isinstance(profile, dict) else "N/A"
                nitro = "✅" if (isinstance(profile, dict) and profile.get("premium_type")) else "❌"
                info  = (
                    f"```\n👤 유저 정보\n━━━━━━━━━━━━━━━━━━━━\n"
                    f"이름: {user.name}#{user.discriminator}\nID: {user.id}\n"
                    f"봇 여부: {'✅' if user.bot else '❌'}\n"
                    f"계정 생성일: {user.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"뱃지: {', '.join(badges) or 'N/A'}\n"
                    f"바이오: {bio}\n니트로: {nitro}\n"
                )
                if member:
                    info += (
                        f"서버 닉네임: {member.nick or 'N/A'}\n"
                        f"서버 입장일: {member.joined_at.strftime('%Y-%m-%d %H:%M:%S') if member.joined_at else 'N/A'}\n"
                        f"역할: {', '.join(r.name for r in member.roles[1:]) or 'N/A'}\n"
                        f"상태: {str(member.status)}\n"
                    )
                info += "━━━━━━━━━━━━━━━━━━━━\n```"
                await message.channel.send(info)
            except Exception as e:
                self.log(f"❌ 유저정보 명령어 에러: {type(e).__name__}: {e}")
                await message.channel.send(f"❌ 유저정보 조회 실패: `{type(e).__name__}: {e}`")

        elif cmd == f"{p}프사":
            if not message.mentions:
                await message.channel.send("사용법: !프사 <@맨션>"); return
            u = message.mentions[0]
            await message.channel.send(f"🖼️ **{u.name}** 의 프로필 사진:\n{u.display_avatar.url}")

        elif cmd == f"{p}배너":
            if not message.mentions:
                await message.channel.send("사용법: !배너 <@맨션>"); return
            u = message.mentions[0]
            try:
                d = await self.http.get_user(u.id)
                banner = d.get("banner")
                if banner:
                    ext = "gif" if banner.startswith("a_") else "png"
                    await message.channel.send(
                        f"🎨 **{u.name}** 의 배너:\n"
                        f"https://cdn.discordapp.com/banners/{u.id}/{banner}.{ext}?size=512"
                    )
                else:
                    color = d.get("accent_color")
                    await message.channel.send(
                        f"🎨 배너 없음, 배경색: #{color:06X}" if color else "❌ 배너가 없습니다."
                    )
            except Exception as e:
                self.log(f"❌ 배너 명령어 에러: {type(e).__name__}: {e}")
                await message.channel.send(f"❌ 배너 조회 실패: `{type(e).__name__}: {e}`")

        elif cmd == f"{p}토큰조회":
            if len(args) < 2:
                await message.channel.send("사용법: !토큰조회 <토큰>"); return
            tok = args[1]
            async with DiscordSession(tok, self.proxy_manager) as s:
                async with s.get("https://discord.com/api/v9/users/@me") as r:
                    if r.status != 200:
                        await message.channel.send("❌ 유효하지 않은 토큰입니다."); return
                    d = await r.json()
                async with s.get("https://discord.com/api/v9/users/@me/billing/payment-sources") as r2:
                    billing = await r2.json() if r2.status == 200 else []
            nitro_map = {0:"없음", 1:"Nitro Classic", 2:"Nitro", 3:"Nitro Basic"}
            created = discord.Object(id=int(d["id"])).created_at.strftime("%Y-%m-%d %H:%M:%S") if d.get("id") else "N/A"
            await message.channel.send(
                f"```\n🔑 토큰 정보\n━━━━━━━━━━━━━━━━━━━━\n"
                f"유저명: {d.get('username')}#{d.get('discriminator')}\nID: {d.get('id')}\n"
                f"이메일: {d.get('email','N/A')}\n전화번호: {d.get('phone','N/A')}\n"
                f"MFA: {'✅' if d.get('mfa_enabled') else '❌'}\n"
                f"니트로: {nitro_map.get(d.get('premium_type',0),'알 수 없음')}\n"
                f"결제수단: {len(billing)}개 등록됨\n"
                f"인증여부: {'✅' if d.get('verified') else '❌'}\n"
                f"계정생성: {created}\n━━━━━━━━━━━━━━━━━━━━\n```"
            )

        elif cmd == f"{p}ip":
            if len(args) < 2:
                await message.channel.send("사용법: !ip <ip주소>"); return
            ip = args[1]
            async with aiohttp.ClientSession() as s:
                async with s.get(f"http://ip-api.com/json/{ip}?fields=66846719") as r:
                    d1 = await r.json()
                async with s.get(f"https://ipwhois.app/json/{ip}") as r2:
                    d2 = await r2.json() if r2.status == 200 else {}
            await message.channel.send(
                f"```\n🌐 IP 정보: {ip}\n━━━━━━━━━━━━━━━━━━━━\n"
                f"국가: {d1.get('country','N/A')} ({d1.get('countryCode','N/A')})\n"
                f"지역: {d1.get('regionName','N/A')} ({d1.get('region','N/A')})\n"
                f"도시: {d1.get('city','N/A')}\n우편번호: {d1.get('zip','N/A')}\n"
                f"위도/경도: {d1.get('lat','N/A')}, {d1.get('lon','N/A')}\n"
                f"시간대: {d1.get('timezone','N/A')}\n"
                f"ISP: {d1.get('isp','N/A')}\n조직: {d1.get('org','N/A')}\n"
                f"AS: {d1.get('as','N/A')}\n"
                f"호스팅: {'✅' if d1.get('hosting') else '❌'} | "
                f"프록시: {'✅' if d1.get('proxy') else '❌'} | "
                f"모바일: {'✅' if d1.get('mobile') else '❌'}\n"
                f"통화: {d2.get('currency','N/A')} ({d2.get('currency_code','N/A')})\n"
                f"언어: {d2.get('languages','N/A')}\n━━━━━━━━━━━━━━━━━━━━\n```"
            )
        # ══════════════════════════════════════════════════
        #  MACRO
        # ══════════════════════════════════════════════════

        elif cmd == f"{p}도배":
            if len(args) < 3:
                await message.channel.send("사용법: !도배 <횟수> <문구>"); return
            try: count = min(max(int(args[1]), 1), 15)
            except:
                await message.channel.send("❌ 횟수는 숫자여야 합니다."); return
            text = " ".join(args[2:])
            self.spam_active = True
            for _ in range(count):
                if not self.spam_active: break
                try:
                    await self.safe_send(message.channel, text)
                except discord.HTTPException as e:
                    if e.status == 429:
                        await asyncio.sleep(getattr(e, "retry_after", 5))
                        await self.safe_send(message.channel, text, skip_typing=True)
                await asyncio.sleep(random.uniform(0.7, 1.5))

        elif cmd == f"{p}도배중지":
            self.spam_active = False
            await message.channel.send("🛑 도배 중지됨")

        elif cmd == f"{p}자동메세지":
            if len(args) < 2:
                await message.channel.send("사용법: !자동메세지 <메시지>"); return
            self.auto_message = " ".join(args[1:])
            self.auto_message_active = True
            await message.channel.send(f"✅ 자동 메세지 설정됨: `{self.auto_message}`")

        elif cmd == f"{p}자동메세지종료":
            self.auto_message_active = False
            self.auto_message = None
            await message.channel.send("🛑 자동메세지 종료됨")

        elif cmd == f"{p}mimic":
            if not message.mentions:
                await message.channel.send("사용법: !mimic <@맨션>"); return
            self.mimic_target = message.mentions[0].id
            self.mimic_active = True
            await message.channel.send(f"✅ {message.mentions[0].display_name} 채팅 따라하기 시작")

        elif cmd == f"{p}stopmimic":
            self.mimic_active = False
            self.mimic_target = None
            await message.channel.send("🛑 mimic 중지됨")

        elif cmd == f"{p}자동이모지반응":
            if len(args) < 2 or not message.mentions:
                await message.channel.send("사용법: !자동이모지반응 <이모지> <@맨션>"); return
            self.auto_emoji = args[1]
            self.auto_emoji_target = message.mentions[0].id
            self.auto_emoji_active = True
            await message.channel.send(f"✅ {message.mentions[0].display_name} → {args[1]} 자동 반응 시작")

        elif cmd == f"{p}자동이모지종료":
            self.auto_emoji_active = False
            self.auto_emoji_target = None
            self.auto_emoji = None
            await message.channel.send("🛑 자동이모지 종료됨")

        # ══════════════════════════════════════════════════
        #  SERVER MANAGE
        # ══════════════════════════════════════════════════

        elif cmd == f"{p}탐아":
            if not message.mentions or len(args) < 3:
                await message.channel.send("사용법: !탐아 <@맨션> <시간(분)> <사유>"); return
            target = message.mentions[0]
            try: minutes = int(args[2])
            except:
                await message.channel.send("❌ 시간은 숫자여야 합니다."); return
            reason = " ".join(args[3:]) if len(args) > 3 else "사유 없음"
            member = message.guild.get_member(target.id)
            if not member:
                await message.channel.send("❌ 멤버를 찾을 수 없습니다."); return
            until = discord.utils.utcnow() + datetime.timedelta(minutes=minutes)
            try:
                await member.timeout(until, reason=reason)
                try: await member.send(f"⏱️ **{message.guild.name}** 에서 **{minutes}분** 타임아웃.\n사유: {reason}")
                except: pass
                await message.channel.send(f"✅ {target.mention} {minutes}분 타임아웃. 사유: {reason}")
            except discord.Forbidden:
                await message.channel.send("❌ 권한이 없습니다.")

        elif cmd == f"{p}탐아해제":
            if not message.mentions:
                await message.channel.send("사용법: !탐아해제 <@맨션> <사유>"); return
            target = message.mentions[0]
            reason = " ".join(args[2:]) if len(args) > 2 else "사유 없음"
            member = message.guild.get_member(target.id)
            if not member:
                await message.channel.send("❌ 멤버를 찾을 수 없습니다."); return
            try:
                await member.timeout(None, reason=reason)
                try: await member.send(f"✅ **{message.guild.name}** 타임아웃 해제.\n사유: {reason}")
                except: pass
                await message.channel.send(f"✅ {target.mention} 타임아웃 해제. 사유: {reason}")
            except discord.Forbidden:
                await message.channel.send("❌ 권한이 없습니다.")

        elif cmd == f"{p}추방":
            if not message.mentions:
                await message.channel.send("사용법: !추방 <@맨션> <사유>"); return
            target = message.mentions[0]
            reason = " ".join(args[2:]) if len(args) > 2 else "사유 없음"
            member = message.guild.get_member(target.id)
            if not member:
                await message.channel.send("❌ 멤버를 찾을 수 없습니다."); return
            try: await member.send(f"👢 **{message.guild.name}** 에서 추방되었습니다.\n사유: {reason}")
            except: pass
            try:
                await member.kick(reason=reason)
                await message.channel.send(f"✅ {target.mention} 추방 완료. 사유: {reason}")
            except discord.Forbidden:
                await message.channel.send("❌ 권한이 없습니다.")

        elif cmd == f"{p}차단":
            if not message.mentions:
                await message.channel.send("사용법: !차단 <@맨션> <사유>"); return
            target = message.mentions[0]
            reason = " ".join(args[2:]) if len(args) > 2 else "사유 없음"
            member = message.guild.get_member(target.id)
            if member:
                try: await member.send(f"🔨 **{message.guild.name}** 에서 차단되었습니다.\n사유: {reason}")
                except: pass
            try:
                await message.guild.ban(target, reason=reason, delete_message_days=0)
                await message.channel.send(f"✅ {target.mention} 차단 완료. 사유: {reason}")
            except discord.Forbidden:
                await message.channel.send("❌ 권한이 없습니다.")

        elif cmd == f"{p}전체청소":
            if len(args) < 2:
                await message.channel.send("사용법: !전체청소 <갯수>"); return
            try: count = min(max(int(args[1]), 1), 30)
            except:
                await message.channel.send("❌ 갯수는 숫자여야 합니다."); return
            deleted = 0
            async for msg in message.channel.history(limit=count + 1):
                try:
                    await msg.delete()
                    deleted += 1
                    await asyncio.sleep(random.uniform(0.5, 1.2))
                except: pass
            confirm = await message.channel.send(f"✅ {deleted}개 메시지 삭제됨")
            await asyncio.sleep(3)
            try: await confirm.delete()
            except: pass

        elif cmd == f"{p}개인청소":
            if len(args) < 2:
                await message.channel.send("사용법: !개인청소 <갯수>"); return
            try: count = min(max(int(args[1]), 1), 30)
            except:
                await message.channel.send("❌ 갯수는 숫자여야 합니다."); return
            deleted = 0
            async for msg in message.channel.history(limit=500):
                if msg.author.id == self.user.id:
                    try:
                        await msg.delete()
                        deleted += 1
                        await asyncio.sleep(random.uniform(0.5, 1.2))
                    except: pass
                    if deleted >= count: break
            confirm = await message.channel.send(f"✅ 내 메시지 {deleted}개 삭제됨")
            await asyncio.sleep(3)
            try: await confirm.delete()
            except: pass

        elif cmd == f"{p}역할":
            if not message.mentions or len(args) < 3:
                await message.channel.send("사용법: !역할 <@맨션> <역할id>"); return
            try: role_id = int(args[2])
            except:
                await message.channel.send("❌ 올바른 역할 ID를 입력해주세요."); return
            role   = message.guild.get_role(role_id)
            member = message.guild.get_member(message.mentions[0].id)
            if not role or not member:
                await message.channel.send("❌ 역할 또는 멤버를 찾을 수 없습니다."); return
            try:
                await member.add_roles(role)
                await message.channel.send(f"✅ {message.mentions[0].mention} 에게 **{role.name}** 역할 부여 완료")
            except discord.Forbidden:
                await message.channel.send("❌ 권한이 없습니다.")

        elif cmd == f"{p}역할롤":
            if len(args) < 2:
                await message.channel.send("사용법: !역할롤 <역할id>"); return
            try: role_id = int(args[1])
            except:
                await message.channel.send("❌ 올바른 역할 ID를 입력해주세요."); return
            role = message.guild.get_role(role_id)
            if not role:
                await message.channel.send("❌ 역할을 찾을 수 없습니다."); return
            ok, fail = 0, 0
            for member in message.guild.members:
                if role not in member.roles:
                    try:
                        await member.add_roles(role)
                        ok += 1
                        await asyncio.sleep(random.uniform(1.5, 3.0))
                    except: fail += 1
            await message.channel.send(f"✅ 역할 부여 완료: 성공 {ok}명 / 실패 {fail}명")
        # ══════════════════════════════════════════════════
        #  RPC
        # ══════════════════════════════════════════════════

        elif cmd == f"{p}실행" or cmd == f"{p}rpc시작":
            self.rpc_active = True
            await self._update_rpc()
            await message.channel.send("✅ RPC 실행됨")

        elif cmd == f"{p}종료" or cmd == f"{p}rpc종료":
            self.rpc_active = False
            await self.change_presence(activity=None)
            await message.channel.send("🛑 RPC 종료됨")

        elif cmd == f"{p}제목":
            if len(args) < 2:
                await message.channel.send("사용법: !제목 <문구>"); return
            self.rpc_data["title"] = " ".join(args[1:])
            if self.rpc_active: await self._update_rpc()
            await message.channel.send(f"✅ RPC 제목 변경됨: `{self.rpc_data['title']}`")

        elif cmd == f"{p}부제목":
            if len(args) < 2:
                await message.channel.send("사용법: !부제목 <문구>"); return
            self.rpc_data["subtitle"] = " ".join(args[1:])
            if self.rpc_active: await self._update_rpc()
            await message.channel.send(f"✅ RPC 부제목 변경됨: `{self.rpc_data['subtitle']}`")

        elif cmd == f"{p}사진변경":
            if len(args) < 2:
                await message.channel.send("사용법: !사진변경 <url>"); return
            self.rpc_data["image"] = args[1].strip()
            if self.rpc_active: await self._update_rpc()
            await message.channel.send("✅ RPC 이미지 변경됨")

        elif cmd == f"{p}링크변경":
            if len(args) < 3:
                await message.channel.send("사용법: !링크변경 <링크1> <링크2>"); return
            self.rpc_data["button1_url"] = args[1]
            self.rpc_data["button2_url"] = args[2]
            if self.rpc_active: await self._update_rpc()
            await message.channel.send("✅ RPC 링크 변경됨")

        elif cmd == f"{p}박스이름변경":
            if len(args) < 3:
                await message.channel.send("사용법: !박스이름변경 <이름1> <이름2>"); return
            self.rpc_data["button1_label"] = args[1]
            self.rpc_data["button2_label"] = args[2]
            if self.rpc_active: await self._update_rpc()
            await message.channel.send(f"✅ RPC 박스 이름 변경됨: `{args[1]}`, `{args[2]}`")

        # ══════════════════════════════════════════════════
        #  PROMO (ADVERTISING)
        # ══════════════════════════════════════════════════

        elif cmd == f"{p}홍보문구":
            if len(args) < 2:
                await message.channel.send("사용법: !홍보문구 <문구>"); return
            self.promo_message = " ".join(args[1:])
            await message.channel.send(f"✅ 홍보 문구가 저장되었습니다:\n`{self.promo_message}`")

        elif cmd == f"{p}홍보시작":
            if len(args) < 2:
                await message.channel.send("사용법: !홍보시작 <분>"); return
            if not self.promo_message:
                await message.channel.send("❌ 먼저 !홍보문구 명령어로 홍보 문구를 설정해주세요."); return
            try:
                minutes = float(args[1])
                if minutes < 5:
                    await message.channel.send("⚠️ 안전을 위해 최소 5분 이상으로 설정해주세요.")
                    minutes = 5.0
                if minutes <= 0: raise ValueError()
            except ValueError:
                await message.channel.send("❌ 올바른 시간(분)을 입력해주세요."); return

            self._stop_promo(message.channel.id)
            task = asyncio.create_task(self._promo_loop(message.channel, minutes))
            self.promo_tasks[message.channel.id] = task
            await message.channel.send(f"✅ 이 채널에서 {minutes}분 간격으로 홍보를 시작합니다.")

        elif cmd == f"{p}홍보중지":
            if message.channel.id in self.promo_tasks:
                self._stop_promo(message.channel.id)
                await message.channel.send("🛑 이 채널의 홍보를 중지했습니다.")
            else:
                await message.channel.send("❌ 이 채널에서 진행 중인 홍보가 없습니다.")

        elif cmd == f"{p}홍보목록":
            msg = self.promo_message or "설정 안 됨"
            active_channels = list(self.promo_tasks.keys())
            channels_str = ", ".join(f"<#{cid}> ({cid})" for cid in active_channels) if active_channels else "없음"
            await message.channel.send(
                f"```\n📩 홍보 정보 목록\n━━━━━━━━━━━━━━━━━━━━\n"
                f"📝 홍보 문구: {msg}\n"
                f"📢 홍보 중인 채널: {channels_str}\n"
                f"━━━━━━━━━━━━━━━━━━━━\n```"
            )

        # ══════════════════════════════════════════════════
        #  PROXY MANAGEMENT
        # ══════════════════════════════════════════════════

        elif cmd == f"{p}프록시목록":
            count = self.proxy_manager.get_count()
            if count == 0:
                await message.channel.send("```🔄 프록시 목록\n━━━━━━━━━━━━━━━━━━━━\n프록시 없음 (직접 연결 모드)\n━━━━━━━━━━━━━━━━━━━━```")
            else:
                proxy_list = self.proxy_manager.get_list_display()
                display = "\n".join(f"  {i+1}. {p}" for i, p in enumerate(proxy_list))
                await message.channel.send(
                    f"```🔄 프록시 목록 ({count}개)\n━━━━━━━━━━━━━━━━━━━━\n{display}\n━━━━━━━━━━━━━━━━━━━━```"
                )

        elif cmd == f"{p}프록시체크":
            count = self.proxy_manager.get_count()
            if count == 0:
                await message.channel.send("❌ 체크할 프록시가 없습니다."); return
            await message.channel.send(f"🔍 프록시 {count}개 체크 중...")
            alive, dead = await self.proxy_manager.check_all()
            await message.channel.send(
                f"```🔄 프록시 체크 완료\n━━━━━━━━━━━━━━━━━━━━\n✅ 생존: {alive}개\n❌ 죽음: {dead}개 (자동 삭제됨)\n📊 남은 프록시: {self.proxy_manager.get_count()}개\n━━━━━━━━━━━━━━━━━━━━```"
            )

        elif cmd == f"{p}프록시리로드":
            self.proxy_manager.reload()
            await message.channel.send(f"✅ 프록시 리로드 완료! ({self.proxy_manager.get_count()}개 로드됨)")

    # ── nitro sniper (on delete) ───────────────────────────
    async def on_message_delete(self, message):
        if not self.sniper_active: return
        codes = re.findall(r'discord\.gift/([a-zA-Z0-9]+)', message.content or "")
        for code in codes:
            await asyncio.sleep(random.uniform(3.0, 8.0))  # Anti-detection delay
            try:
                async with DiscordSession(self.config["token"], self.proxy_manager) as s:
                    async with s.post(
                        f"https://discord.com/api/v9/entitlements/gift-codes/{code}/redeem"
                    ) as r:
                        result = await r.json()
                        ch = self.get_channel(message.channel.id)
                        if ch:
                            if r.status == 200:
                                await ch.send(f"✅ 니트로 스나이핑 성공! `{code}`")
                            else:
                                await ch.send(f"❌ 실패: `{code}` - {result}")
            except Exception as e:
                self.log(f"니트로 스나이핑 에러: {e}")

    # ── RPC helper ────────────────────────────────────────
    async def _update_rpc(self):
        rpc = self.rpc_data
        try:
            image_url = rpc.get("image") or ""
            assets = discord.ActivityAssets(large_image=image_url) if image_url else None
            activity = discord.Activity(
                type=discord.ActivityType.playing,
                name=rpc["title"],
                details=rpc["subtitle"],
                assets=assets,
                buttons=[
                    discord.ActivityButton(label=rpc["button1_label"], url=rpc["button1_url"]),
                    discord.ActivityButton(label=rpc["button2_label"], url=rpc["button2_url"]),
                ]
            )
            await self.change_presence(activity=activity)
        except Exception as e:
            self.log(f"❌ RPC 업데이트 실패: {e}")

# ==============================================================================
# BACKGROUND RUNNER THREAD FOR SELFBOT
# ==============================================================================
class SelfBotThread(QThread):
    log_signal = pyqtSignal(str)
    bot_finished = pyqtSignal()

    def __init__(self, token, config_data, proxy_manager=None):
        super().__init__()
        self.token = token
        self.config_data = config_data
        self.proxy_manager = proxy_manager
        self.client = None

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        self.config_data["token"] = self.token
        self.client = SelfBot(self.log_signal.emit, self.config_data, self.proxy_manager)

        try:
            loop.run_until_complete(self.client.start(self.token))
        except discord.LoginFailure:
            self.log_signal.emit("❌ 로그인 실패: 올바르지 않은 디스코드 토큰이 입력되었습니다. (Improper token has been passed)")
        except Exception as e:
            self.log_signal.emit(f"❌ 셀프봇 구동 중 에러 발생: {e}")
        finally:
            loop.close()
            self.bot_finished.emit()

# ==============================================================================
# MAIN PANEL WINDOW (PyQt6)
# ==============================================================================
class VoltSelfBotPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("파편 셀프봇 패널")
        self.setFixedSize(1100, 700)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        
        self.drag_position = QPoint()
        self.bg_image = QImage()
        
        # Handle __file__ safely for pyinstaller and dynamic execution
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
        except NameError:
            base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
            
        png_path = os.path.join(base_path, "background.png")
        if os.path.exists(png_path):
            self.bg_image.load(png_path)
        self.bot_threads = {}
        self.is_licensed = False
        
        self.config_path = "settings/config.json"
        self.load_configuration()
        
        self.bg_label = QLabel(self)
        self.bg_label.setGeometry(0, 0, 1100, 700)
        self.bg_label.setScaledContents(True)
        
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
        except NameError:
            base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        self.gif_path = os.path.join(base_path, "background.gif")
        self.has_gif = False
        if os.path.exists(self.gif_path):
            self.movie = QMovie(self.gif_path)
            self.bg_label.setMovie(self.movie)
            self.movie.start()
            self.has_gif = True
        else:
            self.bg_label.hide()
            
        self.overlay = QFrame(self)
        self.overlay.setGeometry(0, 0, 1100, 700)
        self.overlay.setStyleSheet("background-color: rgba(10, 10, 15, 120); border: none;")
        
        self.init_ui()
        
    def load_configuration(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    self.config_data = json.load(f)
            except:
                self.config_data = {"prefix": "!", "tokens": [], "account": ""}
        else:
            self.config_data = {"prefix": "!", "tokens": [], "account": ""}
            
    def save_configuration(self):
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            self.append_log(f"설정 파일 저장 실패: {e}")
            
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
            
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
            
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        if not self.has_gif:
            if not self.bg_image.isNull():
                painter.drawImage(self.rect(), self.bg_image)
            else:
                painter.fillRect(self.rect(), QColor(10, 10, 15))
        painter.end()
        
    def get_local_hwid(self):
        if platform.system() == 'Windows':
            try:
                cmd = 'powershell -Command "Get-CimInstance Win32_ComputerSystemProduct | Select-Object -ExpandProperty UUID"'
                output = subprocess.check_output(cmd, shell=True).decode().strip()
                if output and "Error" not in output:
                    return hashlib.sha256(output.encode()).hexdigest()
            except:
                pass
            try:
                cmd = "wmic csproduct get uuid"
                output = subprocess.check_output(cmd, shell=True).decode()
                hwid = output.split('\n')[1].strip()
                if hwid:
                    return hashlib.sha256(hwid.encode()).hexdigest()
            except:
                pass
        return "local_fallback_hwid"
        
    def validate_license(self, key):
        pattern = r"^Volt-\\d{9}-[a-zA-Z]{15}$"
        if not re.match(pattern, key):
            return False, "❌ 올바른 라이선스 형식이 아닙니다.\n(형식: Volt-9자리숫자-15자리영어)"
            
        if BYPASS_AUTH:
            return True, "인증 완료 (로컬 우회 모드)"
            
        if not FIREBASE_AVAILABLE or db_ref is None:
            return False, "❌ Firebase 연결 불가능 (서버 에러)"
            
        try:
            key_info = db_ref.child("volt_keys").child(key).get()
            if not key_info:
                return False, "❌ 유효하지 않은 라이선스 키입니다."
                
            current_hwid = self.get_local_hwid()
            saved_hwid = key_info.get("hwid")
            
            if saved_hwid and saved_hwid != current_hwid:
                return False, "❌ 하드락 차단: 다른 PC에 고정되어 있습니다."
                
            created_at_str = key_info.get("created_at")
            duration_mins = key_info.get("duration_minutes", 0)
            
            if created_at_str:
                created_dt = datetime.datetime.strptime(created_at_str, "%Y-%m-%d %H:%M:%S")
                expire_dt = created_dt + datetime.timedelta(minutes=duration_mins)
                if datetime.datetime.now() > expire_dt:
                    return False, "❌ 만료 기간이 끝난 라이선스입니다."
                    
            if not saved_hwid:
                db_ref.child("volt_keys").child(key).update({"hwid": current_hwid})
                
            return True, "인증 성공"
        except Exception as e:
            return False, f"❌ 인증 실패: {e}"
            
    def init_ui(self):
        self.setStyleSheet(self.styleSheet() + '''
            QWidget {
                font-family: 'Segoe UI', 'Malgun Gothic';
            }
            QPushButton {
                background-color: rgba(255, 255, 255, 15);
                border: 1.5px solid rgba(255, 255, 255, 40);
                border-radius: 8px;
                color: #FFFFFF;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 30);
                border-color: #00E5FF;
            }
            QPushButton:disabled {
                background-color: rgba(255, 255, 255, 5);
                border-color: rgba(255, 255, 255, 10);
                color: rgba(255, 255, 255, 40);
            }
            QLineEdit {
                background-color: rgba(0, 0, 0, 100);
                border: 1.5px solid rgba(255, 255, 255, 30);
                border-radius: 8px;
                color: #FFFFFF;
                padding: 8px 12px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #00E5FF;
            }
            QLineEdit:disabled {
                background-color: rgba(0, 0, 0, 40);
                border-color: rgba(255, 255, 255, 10);
                color: rgba(255, 255, 255, 20);
            }
            QTextEdit {
                background-color: rgba(0, 0, 0, 120);
                border: 1.5px solid rgba(255, 255, 255, 30);
                border-radius: 10px;
                color: #FFFFFF;
                font-family: 'Consolas', monospace;
                font-size: 12px;
                font-weight: bold;
                padding: 10px;
            }
            QTabWidget::pane {
                border: 0;
                background: transparent;
            }
            QTabBar::tab {
                background: rgba(10, 10, 15, 150);
                color: #FFFFFF;
                padding: 8px 20px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: rgba(0, 229, 255, 60);
                color: #FFFFFF;
                border-bottom: 2px solid #00E5FF;
            }
        ''')
        
        master_layout = QVBoxLayout(self)
        master_layout.setContentsMargins(0, 0, 0, 0)
        master_layout.setSpacing(0)
        
        self.tab_widget = QTabWidget(self)
        master_layout.addWidget(self.tab_widget)
        
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        
        self.tab_widget.addTab(self.tab1, "메인 대시보드 (Dashboard)")
        self.tab_widget.addTab(self.tab2, "AI 커스텀 테마 제작소 (AI Theme Maker)")
        self.tab_widget.addTab(self.tab3, "👥 계정 관리소 (Account Manager)")
        self.tab_widget.addTab(self.tab4, "⚙️ 봇 설정 및 매크로 (Settings & Macro)")
        
        self.init_tab1()
        self.init_tab2()
        self.init_tab3()
        self.init_tab4()
        
        # Auto-bypass license verification on startup
        self.is_licensed = True
        self.license_input.setText("Volt-999999999-BypassedKeyLocal")
        self.license_status.setText("인증 상태: 로컬 우회 인증 완료")
        self.license_status.setStyleSheet("color: #4AFF4A; font-weight: bold;")
        self.token_input.setEnabled(True)
        self.launch_btn.setEnabled(True)
        
        self.proxy_manager = ProxyManager(log_callback=self.append_log)
        
        stored_token = self.config_data.get("token", "")
        if stored_token:
            self.token_input.setText(stored_token)
            self.append_log("💾 저장된 토큰을 자동으로 불러왔습니다.")
        self.append_log(f"🔄 프록시: {self.proxy_manager.get_count()}개 로드됨")
        
    def init_tab1(self):
        tab1_layout = QHBoxLayout(self.tab1)
        tab1_layout.setContentsMargins(0, 0, 0, 0)
        tab1_layout.setSpacing(0)
        
        left_panel = QFrame(self.tab1)
        left_panel.setFixedWidth(380)
        left_panel.setStyleSheet("background-color: rgba(10, 10, 15, 150); border-right: 1px solid rgba(255, 255, 255, 20);")
        
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(30, 40, 30, 40)
        
        window_controls = QHBoxLayout()
        window_controls.setContentsMargins(0, 0, 0, 0)
        window_controls.setSpacing(10)
        window_controls.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        
        close_btn = QPushButton("✕", left_panel)
        close_btn.setFixedSize(28, 28)
        close_btn.setStyleSheet('''
            QPushButton {
                background-color: rgba(255, 74, 74, 30);
                border: 1px solid rgba(255, 74, 74, 60);
                border-radius: 14px;
                color: #FF4A4A;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: rgba(255, 74, 74, 70);
                color: #FFFFFF;
            }
        ''')
        close_btn.clicked.connect(self.close)
        
        minimize_btn = QPushButton("─", left_panel)
        minimize_btn.setFixedSize(28, 28)
        minimize_btn.setStyleSheet('''
            QPushButton {
                background-color: rgba(255, 255, 255, 15);
                border: 1px solid rgba(255, 255, 255, 30);
                border-radius: 14px;
                color: #FFFFFF;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 30);
            }
        ''')
        minimize_btn.clicked.connect(self.showMinimized)
        
        window_controls.addWidget(close_btn)
        window_controls.addWidget(minimize_btn)
        left_layout.addLayout(window_controls)
        left_layout.addSpacing(40)
        
        self.brand_title = QLabel("파편 SELFBOT", left_panel)
        self.brand_title.setStyleSheet("color: #FFFFFF; font-size: 28px; font-weight: 800; letter-spacing: 2px; font-family: 'Segoe UI', 'Malgun Gothic';")
        self.brand_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(self.brand_title)
        
        self.brand_sub = QLabel("Premium Discord Client", left_panel)
        self.brand_sub.setStyleSheet("color: #00E5FF; font-size: 11px; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; font-family: 'Segoe UI', 'Malgun Gothic';")
        self.brand_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(self.brand_sub)
        
        left_layout.addSpacing(50)
        
        left_layout.addWidget(QLabel("🔑 라이선스 인증 (License verification)", left_panel).setStyleSheet("color: #FFFFFF; font-size: 12px; font-weight: bold;"))
        self.license_input = QLineEdit(left_panel)
        self.license_input.setPlaceholderText("Volt-9자리숫자-15자리영어")
        left_layout.addWidget(self.license_input)
        
        left_layout.addSpacing(10)
        
        self.verify_btn = QPushButton("인증하기 (Verify)", left_panel)
        self.verify_btn.setFixedHeight(40)
        self.verify_btn.clicked.connect(self.verify_license_key)
        left_layout.addWidget(self.verify_btn)
        
        self.license_status = QLabel("인증 상태: 대기 중", left_panel)
        self.license_status.setStyleSheet("color: #FFFFFF; font-size: 12px; font-weight: bold; margin-top: 5px;")
        self.license_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(self.license_status)
        
        left_layout.addSpacing(20)
        theme_label = QLabel("🎨 테마 선택 (Theme)", left_panel)
        theme_label.setStyleSheet("color: #FFFFFF; font-size: 12px; font-weight: bold;")
        left_layout.addWidget(theme_label)
        
        self.theme_combo = QComboBox(left_panel)
        self.theme_combo.addItems(["기본 (Default)", "벚꽃 (Cherry Blossom)", "바다 (Summer Sea)", "사이버펑크 (Cyberpunk)", "커스텀 (Custom AI)"])
        self.theme_combo.setStyleSheet("QComboBox { color: white; background-color: rgba(30, 30, 40, 200); border: 1px solid rgba(255,255,255,50); border-radius: 5px; padding: 5px; } "
                                       "QComboBox QAbstractItemView { color: white; background-color: rgb(30, 30, 40); selection-background-color: rgba(255, 255, 255, 50); }")
        
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(self.theme_combo)
        
        self.apply_theme_btn = QPushButton("테마 적용 (Apply)", left_panel)
        self.apply_theme_btn.setFixedHeight(30)
        self.apply_theme_btn.clicked.connect(lambda: self.change_theme(self.theme_combo.currentText()))
        theme_layout.addWidget(self.apply_theme_btn)
        
        left_layout.addLayout(theme_layout)
        
        left_layout.addStretch()
        
        self.dev_info = QLabel("made by k16_hj\nVersion: 1.0.0", left_panel)
        self.dev_info.setStyleSheet("color: #FFFFFF; font-size: 11px; font-weight: bold; font-family: 'Segoe UI', 'Malgun Gothic';")
        self.dev_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(self.dev_info)
        
        tab1_layout.addWidget(left_panel)
        
        right_panel = QFrame(self.tab1)
        self.right_panel = right_panel
        right_panel.setStyleSheet("background-color: rgba(10, 10, 15, 100);")
        
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(40, 40, 40, 40)
        right_layout.setSpacing(15)
        
        self.dashboard_frame = QFrame(right_panel)
        self.dashboard_frame.setStyleSheet("background-color: rgba(255, 255, 255, 10); border-radius: 10px; padding: 10px;")
        dash_layout = QHBoxLayout(self.dashboard_frame)
        
        self.uptime_label = QLabel("⏱️ 구동 시간: 대기 중")
        self.uptime_label.setStyleSheet("color: #FFFFFF; font-weight: bold; font-size: 13px; border: none; background: transparent;")
        
        self.proxy_label = QLabel("🔄 프록시: 0개")
        self.proxy_label.setStyleSheet("color: #FFFFFF; font-weight: bold; font-size: 13px; border: none; background: transparent;")
        
        self.ping_label = QLabel("🏓 핑: -- ms")
        self.ping_label.setStyleSheet("color: #FFFFFF; font-weight: bold; font-size: 13px; border: none; background: transparent;")
        
        dash_layout.addWidget(self.uptime_label)
        dash_layout.addWidget(self.proxy_label)
        dash_layout.addWidget(self.ping_label)
        
        right_layout.addWidget(self.dashboard_frame)
        
        self.dash_timer = QTimer(self)
        self.dash_timer.timeout.connect(self.update_dashboard)
        self.dash_timer.start(1000)
        
        self.log_output = QTextEdit(right_panel)
        self.log_output.setReadOnly(True)
        self.log_output.setPlaceholderText(">> 라이선스 키를 입력하고 인증받은 뒤 토큰을 설정하십시오.")
        right_layout.addWidget(self.log_output, stretch=1)
        
        right_layout.addWidget(QLabel("🔑 디스코드 토큰 입력 (Discord Token)", right_panel).setStyleSheet("color: #FFFFFF; font-size: 12px; font-weight: bold;"))
        
        token_input_layout = QHBoxLayout()
        self.token_input = QLineEdit(right_panel)
        self.token_input.setPlaceholderText("디스코드 유저 계정 토큰을 입력하십시오")
        self.token_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.token_input.setEnabled(False)
        token_input_layout.addWidget(self.token_input)
        
        right_layout.addLayout(token_input_layout)
        
        self.launch_btn = QPushButton("토큰 저장 및 봇 기동 (Save Token & Launch)", right_panel)
        self.launch_btn.setFixedHeight(45)
        self.launch_btn.setEnabled(False)
        self.launch_btn.clicked.connect(self.save_and_launch_bot)
        right_layout.addWidget(self.launch_btn)
        
        tab1_layout.addWidget(right_panel)
        
    def init_tab2(self):
        tab2_layout = QVBoxLayout(self.tab2)
        tab2_layout.setContentsMargins(40, 40, 40, 40)
        tab2_layout.setSpacing(15)
        
        # Title
        title = QLabel("AI 커스텀 테마 제작소 (AI Theme Maker)")
        title.setStyleSheet("color: #FFFFFF; font-size: 24px; font-weight: 800;")
        tab2_layout.addWidget(title)
        
        # API Key UI Removed for Free Version
        # Split layout for chat/prompt and preview
        content_layout = QHBoxLayout()
        
        # Left side: Chat & Prompt
        left_v = QVBoxLayout()
        self.ai_chat = QTextEdit()
        self.ai_chat.setReadOnly(True)
        self.ai_chat.append("AI: 어떤 느낌의 테마를 원하시나요? (예: 여름 바다 느낌)")
        left_v.addWidget(self.ai_chat)
        
        prompt_layout = QHBoxLayout()
        self.ai_prompt = QLineEdit()
        self.ai_prompt.setPlaceholderText("원하는 테마를 입력하세요...")
        prompt_layout.addWidget(self.ai_prompt)
        
        self.generate_btn = QPushButton("생성 (Generate)")
        self.generate_btn.clicked.connect(self.generate_ai_theme)
        prompt_layout.addWidget(self.generate_btn)
        
        left_v.addLayout(prompt_layout)
        content_layout.addLayout(left_v, stretch=1)
        
        # Right side: Preview & Apply
        right_v = QVBoxLayout()
        self.preview_label = QLabel("미리보기 (Preview)")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setStyleSheet("background-color: rgba(0, 0, 0, 100); border: 2px dashed rgba(255, 255, 255, 50); border-radius: 10px;")
        self.preview_label.setMinimumSize(400, 225) # 16:9 ratio approximately
        self.preview_label.setScaledContents(True)
        right_v.addWidget(self.preview_label, stretch=1)
        
        self.apply_custom_btn = QPushButton("이 테마로 적용 (Apply this Theme)")
        self.apply_custom_btn.setEnabled(False)
        self.apply_custom_btn.clicked.connect(self.apply_custom_theme)
        right_v.addWidget(self.apply_custom_btn)
        
        content_layout.addLayout(right_v, stretch=1)
        tab2_layout.addLayout(content_layout, stretch=1)
        
    def init_tab3(self):
        tab3_layout = QVBoxLayout(self.tab3)
        tab3_layout.setContentsMargins(40, 40, 40, 40)
        title = QLabel("👥 계정 관리소 (Account Manager)")
        title.setStyleSheet("color: #FFFFFF; font-size: 24px; font-weight: 800;")
        tab3_layout.addWidget(title)
        
        top_layout = QHBoxLayout()
        self.new_token_input = QLineEdit()
        self.new_token_input.setPlaceholderText("여기에 새로운 디스코드 토큰을 입력하세요")
        self.new_token_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.add_token_btn = QPushButton("토큰 추가")
        self.add_token_btn.clicked.connect(self.add_token)
        
        top_layout.addWidget(self.new_token_input)
        top_layout.addWidget(self.add_token_btn)
        tab3_layout.addLayout(top_layout)
        
        self.token_table = QTableWidget()
        self.token_table.setColumnCount(3)
        self.token_table.setHorizontalHeaderLabels(["Masked Token", "Status", "Action"])
        self.token_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.token_table.setStyleSheet("QTableWidget { background-color: rgba(0,0,0,100); color: white; border: 1px solid rgba(255,255,255,50); } QHeaderView::section { background-color: rgba(30,30,40,200); color: white; }")
        tab3_layout.addWidget(self.token_table)
        
        self.refresh_token_table()

    def add_token(self):
        token = self.new_token_input.text().strip()
        if token:
            tokens = self.config_data.get("tokens", [])
            if token not in tokens:
                tokens.append(token)
                self.config_data["tokens"] = tokens
                self.save_configuration()
                self.new_token_input.clear()
                self.refresh_token_table()

    def refresh_token_table(self):
        tokens = self.config_data.get("tokens", [])
        self.token_table.setRowCount(len(tokens))
        
        for i, token in enumerate(tokens):
            masked = token[:10] + "..." + token[-5:] if len(token) > 15 else "***"
            self.token_table.setItem(i, 0, QTableWidgetItem(masked))
            
            is_running = token in self.bot_threads and self.bot_threads[token].isRunning()
            status_text = "Running" if is_running else "Stopped"
            self.token_table.setItem(i, 1, QTableWidgetItem(status_text))
            
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 0, 0, 0)
            
            btn = QPushButton("정지" if is_running else "시작")
            btn.clicked.connect(lambda checked, t=token: self.toggle_bot(t))
            action_layout.addWidget(btn)
            
            del_btn = QPushButton("삭제")
            del_btn.clicked.connect(lambda checked, t=token: self.delete_token(t))
            action_layout.addWidget(del_btn)
            
            self.token_table.setCellWidget(i, 2, action_widget)

    def toggle_bot(self, token):
        if token in self.bot_threads and self.bot_threads[token].isRunning():
            self.append_log(f"토큰 {token[:10]}... 봇을 정지합니다.")
            if self.bot_threads[token].client:
                import asyncio
                asyncio.run_coroutine_threadsafe(self.bot_threads[token].client.close(), self.bot_threads[token].client.loop)
            self.bot_threads[token].terminate()
            self.bot_threads[token].wait()
            del self.bot_threads[token]
        else:
            self.append_log(f"토큰 {token[:10]}... 봇을 시작합니다.")
            thread = SelfBotThread(token, self.config_data, self.proxy_manager)
            thread.log_signal.connect(self.append_log)
            thread.bot_finished.connect(self.refresh_token_table)
            self.bot_threads[token] = thread
            thread.start()
        self.refresh_token_table()

    def delete_token(self, token):
        if token in self.bot_threads and self.bot_threads[token].isRunning():
            self.toggle_bot(token)
        tokens = self.config_data.get("tokens", [])
        if token in tokens:
            tokens.remove(token)
            self.config_data["tokens"] = tokens
            self.save_configuration()
            self.refresh_token_table()

    def init_tab4(self):
        tab4_layout = QVBoxLayout(self.tab4)
        tab4_layout.setContentsMargins(40, 40, 40, 40)
        title = QLabel("⚙️ 봇 설정 및 매크로 (Settings & Macro)")
        title.setStyleSheet("color: #FFFFFF; font-size: 24px; font-weight: 800;")
        tab4_layout.addWidget(title)
        
        # Global Auto-reply
        ar_layout = QHBoxLayout()
        ar_layout.addWidget(QLabel("자동응답:"))
        self.ar_input = QLineEdit()
        self.ar_input.setPlaceholderText("자동 응답 메시지")
        self.ar_toggle = QCheckBox("ON")
        self.ar_toggle.stateChanged.connect(self.update_macros)
        ar_layout.addWidget(self.ar_input)
        ar_layout.addWidget(self.ar_toggle)
        tab4_layout.addLayout(ar_layout)
        
        # Promo Macro
        pr_layout = QHBoxLayout()
        pr_layout.addWidget(QLabel("홍보 매크로:"))
        self.pr_interval = QLineEdit()
        self.pr_interval.setPlaceholderText("간격 (분)")
        self.pr_interval.setFixedWidth(60)
        self.pr_text = QLineEdit()
        self.pr_text.setPlaceholderText("홍보 문구")
        self.pr_toggle = QCheckBox("ON")
        self.pr_toggle.stateChanged.connect(self.update_macros)
        pr_layout.addWidget(self.pr_interval)
        pr_layout.addWidget(self.pr_text)
        pr_layout.addWidget(self.pr_toggle)
        tab4_layout.addLayout(pr_layout)
        
        # Mimic
        mi_layout = QHBoxLayout()
        mi_layout.addWidget(QLabel("따라하기:"))
        self.mi_id = QLineEdit()
        self.mi_id.setPlaceholderText("타겟 유저 ID")
        self.mi_toggle = QCheckBox("ON")
        self.mi_toggle.stateChanged.connect(self.update_macros)
        mi_layout.addWidget(self.mi_id)
        mi_layout.addWidget(self.mi_toggle)
        tab4_layout.addLayout(mi_layout)
        
        # Spam
        sp_layout = QHBoxLayout()
        sp_layout.addWidget(QLabel("도배:"))
        self.sp_count = QLineEdit()
        self.sp_count.setPlaceholderText("횟수")
        self.sp_count.setFixedWidth(60)
        self.sp_text = QLineEdit()
        self.sp_text.setPlaceholderText("도배 문구")
        self.sp_btn = QPushButton("도배 실행")
        self.sp_btn.clicked.connect(self.trigger_spam)
        sp_layout.addWidget(self.sp_count)
        sp_layout.addWidget(self.sp_text)
        sp_layout.addWidget(self.sp_btn)
        tab4_layout.addLayout(sp_layout)
        
        tab4_layout.addStretch()

    def update_macros(self):
        # Update running bots with macro settings
        for token, thread in self.bot_threads.items():
            if thread.isRunning() and thread.client:
                client = thread.client
                # Auto-reply
                if self.ar_toggle.isChecked():
                    client.auto_message = self.ar_input.text()
                    client.auto_message_active = True
                else:
                    client.auto_message_active = False
                
                # Mimic
                if self.mi_toggle.isChecked() and self.mi_id.text().isdigit():
                    client.mimic_target = int(self.mi_id.text())
                    client.mimic_active = True
                else:
                    client.mimic_active = False
                    
                # Note: Promo Macro logic needs to be attached to a specific channel.
                # Global GUI implementation usually applies to a target, but here we just store it in config.
                
    def trigger_spam(self):
        self.append_log("GUI 도배 실행은 !도배 명령어를 사용하는 것을 권장합니다.")
        # Full GUI spam requires channel context, so we just log it.
        
    def save_openai_key(self):
        key = self.openai_key_input.text().strip()
        if key:
            self.config_data["openai_key"] = key
            self.save_configuration()
            self.ai_chat.append("시스템: OpenAI API 키가 저장되었습니다.")
            
    def generate_ai_theme(self):
        prompt = self.ai_prompt.text().strip()
        
        if not prompt:
            self.ai_chat.append("시스템: 프롬프트를 입력해주세요.")
            return
            
        self.ai_chat.append(f"사용자: {prompt}")
        self.ai_chat.append("AI: 완전 무료 AI 서버에서 그림을 그리고 있습니다. 5~10초 정도 기다려주세요...")
        self.generate_btn.setEnabled(False)
        
        # Background generation
        self.ai_thread = AIGeneratorThread(prompt)
        self.ai_thread.result_signal.connect(self.on_ai_result)
        self.ai_thread.error_signal.connect(self.on_ai_error)
        self.ai_thread.start()
        
    def on_ai_result(self, pixmap, url):
        self.generated_pixmap = pixmap
        self.preview_label.setPixmap(pixmap)
        self.ai_chat.append("AI: 테마 생성이 완료되었습니다! 미리보기를 확인해주세요.")
        self.generate_btn.setEnabled(True)
        self.apply_custom_btn.setEnabled(True)
        
    def on_ai_error(self, err_msg):
        self.ai_chat.append(f"AI 오류: {err_msg}")
        self.generate_btn.setEnabled(True)
        
    def apply_custom_theme(self):
        if not hasattr(self, 'generated_pixmap') or self.generated_pixmap.isNull():
            return
            
        theme_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "themes")
        os.makedirs(theme_dir, exist_ok=True)
        custom_path = os.path.join(theme_dir, "custom.png")
        
        self.generated_pixmap.save(custom_path)
        self.ai_chat.append("시스템: 커스텀 테마가 저장되고 적용되었습니다.")
        
        self.theme_combo.setCurrentText("커스텀 (Custom AI)")
        self.change_theme("커스텀 (Custom AI)")
            
    def append_log(self, text):
        timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
        self.log_output.append(f"{timestamp} {text}")
        
    def verify_license_key(self):
        key = self.license_input.text().strip()
        self.append_log("라이선스 검증 시작...")
        
        success, message = self.validate_license(key)
        
        if success:
            self.is_licensed = True
            self.license_status.setText("인증 상태: 인증 완료")
            self.license_status.setStyleSheet("color: #4AFF4A; font-weight: bold;")
            self.append_log(f"✅ {message}")
            
            self.token_input.setEnabled(True)
            self.launch_btn.setEnabled(True)
            
            stored_token = self.config_data.get("token", "")
            if stored_token:
                self.token_input.setText(stored_token)
        else:
            self.is_licensed = False
            self.license_status.setText("인증 상태: 인증 실패")
            self.license_status.setStyleSheet("color: #FF4A4A; font-weight: bold;")
            self.append_log(f"❌ {message}")
            
            self.token_input.setEnabled(False)
            self.launch_btn.setEnabled(False)
            
    def save_and_launch_bot(self):
        token = self.token_input.text().strip()
        if not token:
            self.append_log("❌ 오류: 토큰을 입력하십시오.")
            return
            
        self.config_data["token"] = token
        
        tokens = self.config_data.setdefault("tokens", [])
        if token not in tokens:
            tokens.append(token)
            if hasattr(self, 'refresh_token_table'):
                self.refresh_token_table()
                
        self.save_configuration()
        
        try:
            with open("settings/tokens.txt", "w", encoding="utf-8") as f:
                f.write(token + "\n")
            self.append_log("💾 토큰이 tokens.txt에 저장되었습니다.")
        except Exception as e:
            self.append_log(f"❌ tokens.txt 저장 실패: {e}")
            
        if token in self.bot_threads and self.bot_threads[token].isRunning():
            self.append_log("기존 구동 중인 셀프봇을 정지합니다...")
            self.bot_threads[token].stop()
            self.bot_threads[token].wait()
            del self.bot_threads[token]
            
        self.append_log("🚀 셀프봇 기동을 시작합니다. 디스코드 계정에 접속 중...")
        
        thread = SelfBotThread(token, self.config_data, self.proxy_manager)
        thread.log_signal.connect(self.append_log)
        thread.bot_finished.connect(self.on_bot_thread_finished)
        self.bot_threads[token] = thread
        thread.start()
        
        if hasattr(self, 'refresh_token_table'):
            self.refresh_token_table()
        
    def on_bot_thread_finished(self):
        self.append_log("🛑 봇 스레드 실행이 종료되었습니다.")
        if hasattr(self, 'refresh_token_table'):
            self.refresh_token_table()

    def update_dashboard(self):
        if hasattr(self, 'proxy_manager'):
            self.proxy_label.setText(f"🔄 프록시: {self.proxy_manager.get_count()}개")
        
        running_bots = [t for t in self.bot_threads.values() if t.isRunning() and hasattr(t, 'client') and t.client and t.client.is_ready()]
        
        if running_bots:
            uptime_seconds = int(max(time.time() - getattr(bot.client, 'start_time', time.time()) for bot in running_bots))
            hrs = uptime_seconds // 3600
            mins = (uptime_seconds % 3600) // 60
            secs = uptime_seconds % 60
            self.uptime_label.setText(f"⏱️ 구동 시간: {hrs:02d}:{mins:02d}:{secs:02d}")
            
            import math
            pings = [
                bot.client.latency for bot in running_bots
                if getattr(bot.client, 'latency', None) is not None
                and math.isfinite(bot.client.latency)
            ]
            avg_ping = round(sum(pings) / len(pings) * 1000) if pings else 0
            self.ping_label.setText(f"🏓 핑: {avg_ping} ms (평균)")
        else:
            self.uptime_label.setText("⏱️ 구동 시간: 대기 중")
            self.ping_label.setText("🏓 핑: -- ms")

    def change_theme(self, theme_name):
        theme_map = {
            "벚꽃 (Cherry Blossom)": ("themes/cherry.png", "rgba(255, 182, 193, 40)", "rgba(255, 182, 193, 20)"),
            "바다 (Summer Sea)": ("themes/sea.png", "rgba(0, 105, 148, 40)", "rgba(0, 105, 148, 20)"),
            "사이버펑크 (Cyberpunk)": ("themes/cyberpunk.png", "rgba(138, 43, 226, 40)", "rgba(138, 43, 226, 20)"),
            "커스텀 (Custom AI)": ("themes/custom.png", "rgba(10, 10, 15, 120)", "rgba(10, 10, 15, 100)"),
            "기본 (Default)": (None, "rgba(10, 10, 15, 180)", "rgba(10, 10, 15, 100)")
        }
        
        if theme_name in theme_map:
            img_path, overlay_color, right_panel_color = theme_map[theme_name]
            
            if img_path:
                full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), img_path)
                if os.path.exists(full_path):
                    self.bg_image.load(full_path)
                    self.has_gif = False
                    self.bg_label.hide()
                else:
                    self.append_log(f"⚠️ 테마 이미지를 찾을 수 없습니다: {full_path}")
            else:
                png_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "background.png")
                if os.path.exists(png_path):
                    self.bg_image.load(png_path)
                else:
                    self.bg_image = QImage()
                if hasattr(self, 'gif_path') and os.path.exists(self.gif_path):
                    self.has_gif = True
                    self.bg_label.show()
            
            self.overlay.setStyleSheet(f"background-color: {overlay_color}; border: none;")
            if hasattr(self, 'right_panel'):
                self.right_panel.setStyleSheet(f"background-color: {right_panel_color};")
            self.update()

class AIGeneratorThread(QThread):
    result_signal = pyqtSignal(QPixmap, str)
    error_signal = pyqtSignal(str)
    
    def __init__(self, prompt):
        super().__init__()
        self.prompt = prompt
        
    def run(self):
        import requests
        import urllib.parse
        try:
            full_prompt = self.prompt + ", beautiful anime style illustration, 2D art, aesthetic anime background, not realistic, no photos, dark overlay friendly for a desktop application background"
            encoded_prompt = urllib.parse.quote(full_prompt)
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=576&nologo=true"
            
            response = requests.get(url)
            if response.status_code == 200:
                img_data = response.content
                pixmap = QPixmap()
                pixmap.loadFromData(img_data)
                self.result_signal.emit(pixmap, url)
            else:
                self.error_signal.emit(f"무료 AI 서버 통신 오류: {response.status_code}")
        except Exception as e:
            self.error_signal.emit(f"무료 AI 오류: {str(e)}")
            return

# ==============================================================================
# MAIN EXECUTION ENTRY
# ==============================================================================
if __name__ == "__main__":
    print("[Render] 헤드리스 모드로 셀프봇을 시작합니다.", flush=True)
    
    import os
    _token = os.environ.get("DISCORD_TOKEN")
    
    if not _token:
        if os.path.exists("tokens.txt"):
            with open("tokens.txt", "r") as f:
                _token = f.read().strip()
        else:
            _token = "YOUR_DISCORD_TOKEN_HERE"

    _prefix = "!"

    def _headless_log(msg):
        print(msg, flush=True)

    # 중복 없이 단 한 번만 안전하게 웹 서버를 먼저 실행합니다.
    keep_alive()

    # 복잡한 try/except와 들여쓰기를 모두 제거하여 에러 발생 가능성을 차단합니다.
    _config = {"prefix": _prefix, "token": _token}
    _client = SelfBot(_config, log_callback=_headless_log)
    _client.run(_token)

