const long baudRate = 115200;

void setup() {
	// Start serial and wait for connection
	Serial.begin(baudRate);
	while (!Serial);
	Serial.println("INFO connection_established");
}

// Instruction pointer
int ip = 0;
// Relative base register
long long relBase = 0;
// Number of executed instructions
long instructCount = 0;
// Number of args for each opcode
byte argNums[] = {
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
	long long instruction = get(ip);
	instructCount++;
	byte opcode = instruction % 100;
	if (opcode == 99) {
		halt();
		return;
	}

	// Determine number of args for this opcode
	byte argNum = argNums[opcode];

	// Extract mode for each arg
	byte modes[argNum];
	long long modeVal = instruction / 100;
	long powVal = 1;
	for (int i = 0; i < argNum; i++) {
		// Implicit mode 0 if not specified
		modes[i] = (modeVal / powVal) % 10LL;
		powVal *= 10;
	}

	// ip points to the instruction and first arg is ip+1
	int argAddr[argNum];
	for (int i = 0; i < argNum; i++) {
		int addr = ip + 1 + i;
		switch (modes[i]) {
			case 0:
			// Position mode: The value is the position of the actual value
			argAddr[i] = get(addr);
			break;
		case 1:
			// Immediate mode: The parameter is the value itself
			argAddr[i] = addr;
			break;
		case 2:
			// Relative base mode: The value plus the relative
			// base register is the position of the value
			argAddr[i] = relBase + get(addr);
			break;
		default:
			// Unknown mode
			error("Unknown mode " + String(modes[i]));
			return;
		}
	}

	// moveIP indicates whether the instruction pointer should be moved
	// after execution (for Jump operations this should not be done).
	boolean moveIP = true;

	// Execute instruction
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
				moveIP = false; // Don't move the instruction pointer
				ip = get(argAddr[1]);
			}
			break;
		case 6: // Jump zero
			if (get(argAddr[0]) == 0) {
				moveIP = false; // Don't move the instruction pointer
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
			relBase += get(argAddr[0]);
			break;
		default: // Unknown opcode
			String msg = "Unknown opcode " + String(opcode);
			error(msg);
			return;
	}

	if (moveIP) {
		// Move instruction pointer by one for the instruction (opcode) plus number of args
		ip += 1 + argNum;
	}

	if (instructCount % 100 == 0) {
		// Print the current instruct count every 100 instructions to show that I am still alive
		info("instruction_count_current " + String(instructCount));
	}
}

// Returns the value of the given address in the program
// by querying the control program.
long long get(int addr) {
	Serial.print("GET ");
	Serial.println(addr);
	return readLL();
}

// Sets the address to the given value in the
// program by querying the control program.
void set(int addr, long long val) {
	Serial.print("SET ");
	Serial.print(addr);
	Serial.print(" ");
	printLL(val);
	Serial.println();
	Serial.flush();
}

// Converts a boolean into an integer.
int boolToInt(boolean b) {
	if (b) {
		return 1;
	} else {
		return 0;
	}
}

// Reads a value from the input by querying the control program.
long long input() {
	Serial.println("INPUT");
	return readLL();
}

// Outputs a value by sending it to the control program
void output(long long val) {
	Serial.print("OUTPUT ");
	printLL(val);
	Serial.println();
	Serial.flush();
}

// Sends the final instructCount and halt to controller and resets ip and relBase.
void halt() {
	info("instruct_count_final " + String(instructCount));
	Serial.println("HALT");
	Serial.flush();
	ip = 0;
	relBase = 0;
}

// Sends the message to the controller and calls halt().
void error(String msg) {
	Serial.print("ERROR ");
	Serial.println(msg);
	halt();
}

// Sends a info message to the controller.
void info(String msg) {
	Serial.print("INFO ");
	Serial.println(msg);
}

// Prints a long long to the serial connection.
void printLL(long long x) {
	// Print sign
	if (x < 0) {
		Serial.print("-");
	}
	long long xPos = abs(x);

	// Split long long into two longs and print them separately
	char buffer[10];
	sprintf(buffer, "%06ld", (long)(xPos/1000000L));
	Serial.print(buffer);
	sprintf(buffer, "%06ld", (long)(xPos%1000000L));
	Serial.println(buffer);
}

// Reads a long long from the serial console.
long long readLL() {
	long long num = 0;
	char sign = 1;
	for (int i = 0; ; i++) {
		// Wait for Serial to receive next char
		while (!Serial.available());
		char c = Serial.read();
		if (c == '\n') {
			// Number finished
			break;
		} else if (c == '-') {
			// Change sign to negative
			sign = -1;
		} else {
			// Shift number one decimal place to the left
			num *= 10;
			// Convert ascii to number and add to num
			num += c - '0';
		}
	}
	return sign * num;
}
