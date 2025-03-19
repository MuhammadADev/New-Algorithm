import bitcoin
import os

# Set the starting hexadecimal value
start_hex = "00000000000000000000000000000000000000000000000f0000000000000000"

# Set a flag to indicate whether all the addresses have been found
all_addresses_found = False

# Check if a progress file exists
if os.path.exists("progress.txt"):
    with open("progress.txt", "r") as f:
        start_hex = f.read().strip()

# Convert the starting hexadecimal value to an integer
start_int = int(start_hex, 16)

# Set the ending hexadecimal value
end_hex = "00000000000000000000000000000000000000000000000fffffffffffffffff"
end_int = int(end_hex, 16)

# Load addresses from file
addresses = []
if os.path.exists("address.txt"):
    with open("address.txt", "r") as f:
        addresses = f.read().splitlines()

# Open the output file for writing results
with open("output.txt", "a") as output_file:
    while not all_addresses_found:
        for i in range(start_int, end_int):
            # Convert the integer to a hexadecimal value
            private_key_hex = hex(i)[2:].zfill(64)

            # Generate the public key from the private key
            public_key = bitcoin.privkey_to_pubkey(private_key_hex)

            # Generate the compressed public key
            if public_key[-1] in ['0', '2', '4', '6', '8', 'A', 'C', 'E']:  # Check if y-coordinate is even
                compressed_public_key = '02' + public_key[2:66]  # Prefix with 0x02 and take the x-coordinate
            else:
                compressed_public_key = '03' + public_key[2:66]  # Prefix with 0x03 and take the x-coordinate

            # Generate the Bitcoin address from the compressed public key
            address = bitcoin.pubkey_to_address(compressed_public_key)

            # Log the current address and private key to the output file
            output_file.write(f"Address: {address}\nPrivate key: {private_key_hex}\n")

            # Check if the address exists in the address.txt file
            if address in addresses:
                # Save the address and private key to foundit.txt
                with open("foundit.txt", "a") as f:
                    f.write(f"Address: {address}\nPrivate key: {private_key_hex}\n")

                # Remove the found address from the list of addresses
                addresses.remove(address)

                # If all the addresses have been found, set the flag to True
                if len(addresses) == 0:
                    all_addresses_found = True
                    break

        # Save the last hexadecimal value used to the progress file
        with open("progress.txt", "w") as f:
            f.write(private_key_hex)

# Save the remaining addresses to the address.txt file
if addresses:
    with open("address.txt", "w") as f:
        for address in addresses:
            f.write(address + "\n")
