Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;

public class WinAPI {
    [DllImport("user32.dll", SetLastError = true)]
    public static extern bool SystemParametersInfo(uint uiAction, uint uiParam, IntPtr pvParam, uint fWinIni);
}
"@

$SPI_SETDRAGFULLWINDOWS = 0x0025
$SPIF_UPDATEINIFILE = 0x01
$SPIF_SENDCHANGE = 0x02

$result = [WinAPI]::SystemParametersInfo(
    $SPI_SETDRAGFULLWINDOWS,
    1,
    [IntPtr]::Zero,
    $SPIF_UPDATEINIFILE -bor $SPIF_SENDCHANGE
)

if (-not $result) {
    throw "Erro ao habilitar o recurso DragFullWindows."
}