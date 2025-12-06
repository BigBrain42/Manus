#!/bin/bash

# Supabase Backend - Startup Script
# Startet Backend und Frontend

echo "🚀 Starte Supabase Backend System..."
echo ""

# Farben für Output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Überprüfe, ob Python installiert ist
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 ist nicht installiert"
    exit 1
fi

# Überprüfe, ob pip installiert ist
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 ist nicht installiert"
    exit 1
fi

# Installiere Abhängigkeiten, falls nicht vorhanden
echo -e "${BLUE}📦 Überprüfe Abhängigkeiten...${NC}"
pip3 install -q fastapi uvicorn supabase python-dotenv pydantic

echo ""
echo -e "${GREEN}✓ Abhängigkeiten installiert${NC}"
echo ""

# Starte Backend
echo -e "${BLUE}🔧 Starte Backend auf Port 8000...${NC}"
cd "$(dirname "$0")"
python3 main.py > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}✓ Backend gestartet (PID: $BACKEND_PID)${NC}"

# Warte kurz, damit Backend startet
sleep 2

# Überprüfe, ob Backend läuft
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo -e "${YELLOW}⚠️  Backend scheint nicht zu starten. Überprüfen Sie /tmp/backend.log${NC}"
else
    echo -e "${GREEN}✓ Backend läuft unter http://localhost:8000${NC}"
fi

echo ""

# Starte Frontend
echo -e "${BLUE}🎨 Starte Frontend auf Port 5000...${NC}"
cd "$(dirname "$0")/frontend"
python3 -m http.server 5000 > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!
echo -e "${GREEN}✓ Frontend gestartet (PID: $FRONTEND_PID)${NC}"

# Warte kurz, damit Frontend startet
sleep 1

# Überprüfe, ob Frontend läuft
if ! curl -s http://localhost:5000/index.html > /dev/null; then
    echo -e "${YELLOW}⚠️  Frontend scheint nicht zu starten. Überprüfen Sie /tmp/frontend.log${NC}"
else
    echo -e "${GREEN}✓ Frontend läuft unter http://localhost:5000${NC}"
fi

echo ""
echo -e "${GREEN}════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ Supabase Backend System läuft!${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}📍 Zugriff:${NC}"
echo -e "   Frontend:    ${GREEN}http://localhost:5000${NC}"
echo -e "   Backend API: ${GREEN}http://localhost:8000${NC}"
echo -e "   API Docs:    ${GREEN}http://localhost:8000/docs${NC}"
echo ""
echo -e "${BLUE}📝 Logs:${NC}"
echo -e "   Backend:  /tmp/backend.log"
echo -e "   Frontend: /tmp/frontend.log"
echo ""
echo -e "${BLUE}🛑 Zum Beenden:${NC}"
echo -e "   kill $BACKEND_PID  # Backend stoppen"
echo -e "   kill $FRONTEND_PID # Frontend stoppen"
echo ""

# Warte auf Eingabe zum Beenden
echo -e "${YELLOW}Drücken Sie Ctrl+C zum Beenden...${NC}"
wait
