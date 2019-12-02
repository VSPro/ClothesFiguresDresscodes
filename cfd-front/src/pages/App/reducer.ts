type state = {
    paramsOfUser: {
        shape: string,
        sizeParams: {
            sizeOfChest: string,
            sizeOfHips: string,
            height: number
        }
    }
}

// TODO: уменьшить вложенность или призятять экшены к последним по уровню вложенность значениям
const initialState: state = {
    paramsOfUser: {
        shape: '',
        sizeParams: {
            sizeOfChest: '',
            sizeOfHips: '',
            height: 0
        }
    }
}

export default function appReducer(state = initialState, action: any) {
    switch (action.type) {
        case 'PARAMS_OF_USER':
            return {...state, paramsOfUser: action.payload}
        default:
            return state
    }
}