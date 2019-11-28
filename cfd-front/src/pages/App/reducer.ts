type state = {
    paramsOfUser: {
        shape: string,
        sizeParams: {
            size: string,
            height: number
        }
    }
}

// TODO: уменьшить вложенность или призятять экшены к последним по уровню вложенность значениям
const initialState: state = {
    paramsOfUser: {
        shape: '',
        sizeParams: {
            size: '',
            height: 0
        }
    }
}

export default function appReducer(state = initialState, action: any) {
    switch (action.type) {
        case 'TYPE_OF_SHAPE':
            return {...state, paramsOfUser: action.payload}
        default:
            return state
    }
}