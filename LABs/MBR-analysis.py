def extract_mbr_sections(filename):
    # Define the size of a disk sector
    SECTOR_SIZE = 512  # bytes
    
    # Define the sections of the MBR with their start and end offsets
    sections = {
        "Boot Code": (0x000, 0x1BD),
        "Partition 1": (0x1BE, 0x1CD),
        "Partition 2": (0x1CE, 0x1DD),
        "Partition 3": (0x1DE, 0x1ED),
        "Partition 4": (0x1EE, 0x1FD),
        "Boot Signature": (0x1FE, 0x1FF)
    }
    
    # Open the specified file in binary read mode
    with open(filename, 'rb') as f:
        # Iterate over each section defined in the sections dictionary
        for section, (start, end) in sections.items():
            # Seek to the start of the section
            f.seek(start)
            # Read the bytes from the start to the end of the section
            chunk = f.read(end - start + 1)
            # Convert the bytes to a string of hexadecimal values
            hex_values = " ".join([f"{byte:02x}" for byte in chunk])
            
            # Create an ASCII representation, replacing non-printable characters with '.'
            ascii_values = "".join([chr(byte) if 32 <= byte < 127 else "." for byte in chunk])
            
            # Print the section name, start, and end offsets
            print(f"{section} ({start:#04x} – {end:#04x}):")
            # Print the hexadecimal values and the ASCII representation
            print(hex_values.upper() + "  " + ascii_values)
            
            # If the section is a partition entry, decode its details
            if "Partition" in section:
                # Determine the status of the partition (active/inactive)
                status = "Active" if chunk[0] == 0x80 else "Inactive"
                # Get the partition type
                partition_type = chunk[4]
                # Get the LBA (Logical Block Addressing) address
                lba_address = int.from_bytes(chunk[8:12], 'little')
                # Get the number of sectors in the partition
                number_of_sectors = int.from_bytes(chunk[12:16], 'little')
                
                # Calculate the size of the partition in bytes
                size_in_bytes = number_of_sectors * SECTOR_SIZE
                # Calculate the byte offset for the start of the file system
                byte_offset = lba_address * SECTOR_SIZE
                # Convert the byte offset to a hexadecimal string
                byte_offset_hex = hex(byte_offset)
                
                # Print the decoded partition details
                print(f"  Status: {status}")
                print(f"  Partition Type: {partition_type:#04x}")
                print(f"  LBA Address: {lba_address}")
                print(f"  Number of Sectors: {number_of_sectors}")
                print(f"  Size in bytes: {size_in_bytes}")
                print(f"  Byte offset address for start of file system: {byte_offset} ({byte_offset_hex})")
            
            # Print a blank line for readability
            print()

# Example usage:
# extract_mbr_sections('mbr_image.bin')
