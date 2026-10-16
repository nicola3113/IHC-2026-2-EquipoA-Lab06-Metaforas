#!/bin/sh
# Verificación del Paso 1 en Mozilla Firefox (modo headless, sin Playwright).
# Abre la galería con ?autotest=1 (la página ejecuta su lista de comprobación al cargar)
# y guarda capturas de pantalla. Uso: sh verificar_firefox.sh
FF="$LOCALAPPDATA/Microsoft/WindowsApps/firefox.exe"
RAIZ="$(cd "$(dirname "$0")/../.." && pwd)"
HTML="$(cygpath -m "$RAIZ/L4_paso_a_paso/paso1_galeria/03_version_mejorada/ejercicio_6_1_galeria_metaforas_v2_EquipoA.html")"
CAP="$(cygpath -w "$RAIZ/L4_paso_a_paso/paso1_galeria/capturas")"
PERFIL="$(cygpath -w "${TEMP:-/tmp}")\ff_perfil_galeria"
mkdir -p "$(cygpath -u "$PERFIL")"
"$FF" --version
"$FF" --headless --no-remote --profile "$PERFIL" --window-size=1366,1500 --screenshot "$CAP\v2_verificacion_firefox.png" "file:///$HTML?autotest=1&tema=oscuro" 2>/dev/null
"$FF" --headless --no-remote --profile "$PERFIL" --window-size=1366,900 --screenshot "$CAP\v2_firefox_vista_general.png" "file:///$HTML?tema=oscuro" 2>/dev/null
echo "Capturas en $CAP"
