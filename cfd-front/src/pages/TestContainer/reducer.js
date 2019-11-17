const initialState = {
    testItem: null
}

export default function testReducer(state = initialState, action) {
    switch (action.type) {
        case 'TEST_ITEM':
            return {...state, testItem: action.payload}
        default:
            return state
    }
}