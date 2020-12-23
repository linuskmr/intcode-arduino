void setup() {
  Serial.begin(9600);
  while (!Serial); // wait for Serial port to connect.
  Serial.println("Listening\n");

}

int ip = 0;
long relBase = 0;
long instructCount = 0;
byte argsLen[] = {
  0,
  3, // Add
  3, // Multiplication
  1, // Input
  1, // Output
  2, // Jump non-zero
  2, // Jump zero
  3, // Less than
  3, // Equals
  1  // Change relative base
  };


void loop() {
  // Load next instruction
  long instruction = get(ip);
  instructCount++;
  /*Serial.print("Load next instruction ");
  Serial.print(instruction);
  Serial.print(" on ip ");
  Serial.println(ip);
  Serial.flush();*/
  byte opcode = instruction % 100;
  if (opcode == 99) {
    halt();
    return;
  }

  // Determine number of args for this opcode
  byte argLen = argsLen[opcode];

  // Extract modes
  long modeVal = instruction / 100;
  byte modes[argLen];
  for (int i = 0; i < argLen; i++) {
    modes[i] = (modeVal / ((long) pow(10, i))) % 10;
  }

  // Get memory address for each arg
  int argAddr[argLen];
  for (int i = 0; i < argLen; i++) {
    int addr = ip + i + 1;
    switch (modes[i]) {
      case 0: // Position mode
        argAddr[i] = get(addr);
        break;
      case 1: // Immediate mode
        argAddr[i] = addr;
        break;
      case 2: // Relative base mode
        argAddr[i] = relBase + get(addr);
        break;
      default: // Unknown mode
        error("Unknown mode " + String(modes[i]));
        return;
    }
  }

  // Execute instruction
  boolean moveIP = true;
  switch (opcode) {
    case 1: // Addition
      set(argAddr[2], get(argAddr[0]) + get(argAddr[1]));
      break;
    case 2: // Multiplication
      set(argAddr[2], get(argAddr[0]) * get(argAddr[1]));
      break;
    case 3: // Input
      set(argAddr[0], input());
      break;
    case 4: // Output
      output(get(argAddr[0]));
      break;
    case 5: // Jump non-zero
      if (get(argAddr[0]) != 0) {
        moveIP = false;
        ip = get(argAddr[1]);
      }
      break;
    case 6: // Jump zero
      if (get(argAddr[0]) == 0) {
        moveIP = false;
        ip = get(argAddr[1]);
      }
      break;
    case 7: // Less than
      set(argAddr[2], boolToInt(get(argAddr[0]) < get(argAddr[1])));
      break;
    case 8: // Equals
      set(argAddr[2], boolToInt(get(argAddr[0]) == get(argAddr[1])));
      break;
    case 9: // Change relative base
      relBase = get(argAddr[0]);
      break;
    default: // Unknown opcode
      String msg = "Unknown opcode " + String(opcode);
      //msg.concat();
      error(msg);
      return;
  }

  if (moveIP) {
    ip += 1 + argLen;
  }
  delay(10);
}


long arr[] = {2, 1, 1, 1, 99};

long get(int addr) {
  Serial.print("GET ");
  Serial.println(addr);
  while (!Serial.available());
  String valStr = Serial.readStringUntil('\n');
  /*Serial.print("Received ");
  Serial.print(valStr);
  Serial.println(".");
  Serial.flush();*/
  return valStr.toInt();
}

int boolToInt(boolean b) {
  if (b) {
    return 1;
  } else {
    return 0;
  }
}

long input() {
  Serial.println("INPUT");
  while (!Serial.available());
  String valStr = Serial.readStringUntil('\n');
  return valStr.toInt();
}

void output(long val) {
  Serial.print("OUTPUT ");
  Serial.println(val);
  Serial.flush();
}

void set(int addr, long val) {
  Serial.print("SET ");
  Serial.print(addr);
  Serial.print(" ");
  Serial.println(val);
  Serial.flush();
  arr[addr] = val;
}

void halt() {
  Serial.print("HALT ");
  Serial.print("InstructCount ");
  Serial.println(instructCount);
  Serial.flush();
  ip = 0;
  relBase = 0;
}

void error(String msg) {
  Serial.print("ERROR ");
  Serial.println(msg);
  halt();
}
