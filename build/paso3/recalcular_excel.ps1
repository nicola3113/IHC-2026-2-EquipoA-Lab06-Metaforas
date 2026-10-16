# Recalcula el Excel del Paso 3 con Microsoft Excel (para guardar los valores de las fórmulas)
# y exporta las hojas principales como imagen de evidencia. Uso: powershell -File recalcular_excel.ps1
$d = Join-Path $PSScriptRoot "..\..\L4_paso_a_paso\paso3_medicion" | Resolve-Path
$cap = Join-Path $d "capturas"; New-Item -ItemType Directory -Force $cap | Out-Null
$xl = New-Object -ComObject Excel.Application; $xl.Visible = $false; $xl.DisplayAlerts = $false
try {
  $wb = $xl.Workbooks.Open((Join-Path $d "resultados_6_3_EquipoA.xlsx")); $xl.CalculateFull(); $wb.Save()
  foreach ($n in @("Resumen_por_estilo", "Consolidado")) {
    $s = $wb.Worksheets.Item($n); $s.PageSetup.Orientation = 2; $s.PageSetup.Zoom = $false
    $s.PageSetup.FitToPagesWide = 1; $s.PageSetup.FitToPagesTall = 1
    $s.ExportAsFixedFormat(0, (Join-Path $cap "excel_$n.pdf"))
  }
  $wb.Close($true)
} finally { $xl.Quit(); [System.Runtime.InteropServices.Marshal]::ReleaseComObject($xl) | Out-Null }
