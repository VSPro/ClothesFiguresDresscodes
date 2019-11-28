type params = { 
    shoulders: number, 
    chest: number,
    waist: number, 
    hips: number, 
    height: number, 
    sex: string
}

const listOfSizesByChest_M: number[] = [93, 97, 101, 105, 109, 113] // XS, S, M, L, XL, XXL
const listOfSizesByChest_F: number[] = [81, 89, 97, 107, 119, 131]
const namesOfSizes = ['XS', 'S', 'M', 'L', 'XL', 'XXL']

export default function({chest, height, sex}: params) {
    // Осторожно! Код ниже не оптимален
    let size: string = namesOfSizes[0]
    if (sex === 'm') {
        listOfSizesByChest_M.forEach( (item, index) => {
            if (chest > item) {
                size = namesOfSizes[index]
            } 
        })
    } else {
        listOfSizesByChest_F.forEach( (item, index) => {
            if (chest > item) {
                size = namesOfSizes[index]
            } 
        })
    }

    return {
        size: size,
        height: height
    }
}