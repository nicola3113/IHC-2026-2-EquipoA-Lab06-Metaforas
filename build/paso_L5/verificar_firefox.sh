#!/bin/sh
# L.5 — Verificación del prototipo en Mozilla Firefox (headless): ?autotest=1 y captura del resultado.
FF="$LOCALAPPDATA/Microsoft/WindowsApps/firefox.exe"
RAIZ="$(cd "$(dirname "$0")/../.." && pwd)"
HTML="$(cygpath -m "$RAIZ/L5_metafora_propia/prototipo/L5_huerto_inversiones_EquipoA.html")"
CAP="$(cygpath -w "$RAIZ/L5_metafora_propia/capturas")"
PERFIL="$(cygpath -w "${TEMP:-/tmp}")\ff_perfil_huerto"; mkdir -p "$(cygpath -u "$PERFIL")"
"$FF" --headless --no-remote --profile "$PERFIL" --window-size=1366,1300 --screenshot "$CAP\L5_verificacion_firefox.png" "file:///$HTML?autotest=1" 2>/dev/null
echo "Captura: $CAP\L5_verificacion_firefox.png"
