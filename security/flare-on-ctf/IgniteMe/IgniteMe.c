
char ENCODED[] = "\x0d\x26\x49\x45\x2a\x17\x78\x44\x2b\x6c\x5d\x5e\x45\x12\x2f\x17\x2b\x44\x6f\x6e\x56\x09\x5f\x45\x47\x73\x26\x0a\x0d\x13\x17\x48\x42\x01\x40\x4d\x0c\x02\x69";

void __noreturn start()
{
  DWORD NumberOfBytesWritten; // [sp+0h] [bp-4h]@1

  NumberOfBytesWritten = 0;
  hFile = GetStdHandle(0xFFFFFFF6);
  dword_403074 = GetStdHandle(0xFFFFFFF5);
  WriteFile(dword_403074, aG1v3M3T3hFl4g, 0x13u, &NumberOfBytesWritten, 0);
  sanitize_input();
  if ( check_sanitized_input() )
    WriteFile(dword_403074, aG00dJ0b, 0xAu, &NumberOfBytesWritten, 0);
  else
    WriteFile(dword_403074, aN0tT00H0tRWe_7, 0x24u, &NumberOfBytesWritten, 0);
  ExitProcess(0);
}


signed int sanitize_input()
{
  int v0; // eax@5
  char Buffer[260]; // [sp+0h] [bp-110h]@3
  DWORD NumberOfBytesRead; // [sp+104h] [bp-Ch]@4
  unsigned int i; // [sp+108h] [bp-8h]@1
  char v5; // [sp+10Fh] [bp-1h]@1

  v5 = 0;
  for ( i = 0; i < 0x104; ++i )
    Buffer[i] = 0;
  ReadFile(hFile, Buffer, 0x104u, &NumberOfBytesRead, 0);
  for ( i = 0; ; ++i )
  {
    v0 = get_input_size((int)Buffer);
    if ( i >= v0 )
      break;
    v5 = Buffer[i];
    if ( v5 != 10 && v5 != 13 && v5 != 0)
    {
        G_SANITIZED_BUF[i] = v5;
    }
  }
  return 1;
}


signed int check_sanitized_input()
{
  int v0; // ST04_4@1
  int i; // [sp+4h] [bp-8h]@1
  unsigned int j; // [sp+4h] [bp-8h]@4
  char KEY; // [sp+Bh] [bp-1h]@1

  v0 = get_input_size((int)G_SANITIZED_BUF);
  KEY = 4;

  for ( i = v0 - 1; i >= 0; --i )
  {
    G_OUTPUT_BUF[i] = KEY ^ G_SANITIZED_BUF[i];
    KEY = G_SANITIZED_BUF[i];
  }
  for ( j = 0; j < 0x27; ++j )
  {
    if ( G_OUTPUT_BUF[j] != ENCODED[j] )
      return 0;
  }
  return 1;
}


int __cdecl get_input_size(int offset_adr_buf)
{
  int index_in_buf; // [sp+0h] [bp-4h]@1

  for ( index_in_buf = 0; *(_BYTE *)(index_in_buf + offset_adr_buf); ++index_in_buf )
    ;
  return index_in_buf;
}



__int16 sub_401000()
{
  int v0; // eax@1

  v0 = __ROL4__(0x80070000, 4);
  return (unsigned __int16)v0 >> 1;
}