import random
import bitcoin
import os

# Define the range for the private keys
start_int = int("f7000000000000000", 16)  # Starting value in decimal
end_int = int("fffffffffffffffff", 16)     # Ending value in decimal

# Define the output files
output_file = "Addresses_f_range_5.txt"
found_file = "foundit.txt"
address_file = "address.txt"
previous_addresses_file = "previous_address.txt"

# Load previously generated keys
def load_existing_keys(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            existing_keys = set()
            for line in f:
                line = line.strip()
                if line:  # Only process non-empty lines
                    parts = line.split(",")
                    if len(parts) > 1:  # Ensure there are at least two parts
                        key_part = parts[0].split(": ")
                        if len(key_part) > 1:  # Ensure the key part is valid
                            existing_keys.add(key_part[1])
            return existing_keys
    return set()

# Load previously generated keys and addresses
existing_keys = load_existing_keys(output_file)
previous_addresses = load_existing_keys(previous_addresses_file)
existing_addresses = load_existing_keys(address_file)

# Number of random keys to generate
num_keys_to_generate = 100000  # Change this to generate more or fewer keys

# Set to keep track of generated addresses to avoid duplicates
generated_addresses = set()

# Function to check if the private key is valid
def is_valid_private_key(private_key_hex):
    # Check for consecutive repeating characters
    for i in range(len(private_key_hex) - 1):
        if private_key_hex[i] == private_key_hex[i + 1]:
            return False
    # Check for repeating zeros
    if '00' in private_key_hex:
        return False
    return True

# Collect results to write to the file
results = []

# Generate random keys and save them to the file
for _ in range(num_keys_to_generate):
    # Generate a random integer within the specified range
    random_private_key_int = random.randint(start_int, end_int)
    
    # Convert the integer to a hexadecimal string
    random_private_key_hex = hex(random_private_key_int)[2:].zfill(64)  # Ensure it's 64 characters long

    # Debugging: Print the generated private key
    print(f"Generated Private Key (Hex): {random_private_key_hex}")

    # Check if the key is valid
    if not is_valid_private_key(random_private_key_hex):
        print("Invalid private key, skipping...")
        continue
    
    # Check if the key has already been generated
    if random_private_key_hex in existing_keys:
        print("Private key already exists, skipping...")
        continue
    
    # Generate the public key from the private key
    public_key = bitcoin.privkey_to_pubkey(random_private_key_hex)

    # Generate the compressed public key
    compressed_public_key = ('02' if public_key[-1] in '02468ACE' else '03') + public_key[2:66]

    # Generate the Bitcoin address from the compressed public key
    address = bitcoin.pubkey_to_address(compressed_public_key)

    # Debugging: Print the generated address
    print(f"Generated Address: {address}")

    # Check if the generated address is unique and not in previous_addresses
    if address in previous_addresses or address in generated_addresses:
        print("Address already exists, skipping...")
        continue  # Skip if the address has been generated before

    # Add the address to the set of generated addresses
    generated_addresses.add(address)

    # Collect the private key and address for writing
    results.append(f"Private Key (Hex): {random_private_key_hex}, Address: {address}")

# Write all results to the output file at once
with open(output_file, "w") as f:
    for result in results:
        f.write(result + "\n")

# Print completion message
print(f"Generated {len(results)} valid private keys and their corresponding addresses, saved to {output_file}.")
