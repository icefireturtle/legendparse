def slicer(message, records):
    slices = []
    field_lengths = []

    for data in records:
        field_lengths.append(data.field_length)

    slices.append(message[:field_lengths[0]])

    start = field_lengths[0]
    end = start

    if len(field_lengths) > 2:
        
        for i in range(1, len(field_lengths)):
            end += field_lengths[i]
            slices.append(message[start:end])
            start = end
            
    return slices

