# Abre un .docx con Microsoft Word, actualiza el índice y los campos, guarda y exporta a PDF.
# Uso: powershell -File actualizar_word.ps1 -Docx <ruta.docx>
param([Parameter(Mandatory = $true)][string]$Docx)
$Docx = (Resolve-Path $Docx).Path
$word = New-Object -ComObject Word.Application
$word.Visible = $false; $word.DisplayAlerts = 0
try {
  $doc = $word.Documents.Open($Docx)
  foreach ($toc in $doc.TablesOfContents) { $toc.Update() }
  $doc.Fields.Update() | Out-Null
  foreach ($toc in $doc.TablesOfContents) { $toc.Update() }
  $doc.Save()
  $doc.ExportAsFixedFormat([System.IO.Path]::ChangeExtension($Docx, ".pdf"), 17)
  "Páginas: " + $doc.ComputeStatistics(2)
  $doc.Close($false)
} finally { $word.Quit(); [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null }
