import React, { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { withRouter } from 'react-router-dom'

function TestContainer( props: any ) {

    const dispatch = useDispatch()
    const testData = useSelector( (store: any) => store.test.testItem )

    // console.log('I\'m called from TestContainer component', props)

    return <>
        <button
            onClick={() => { dispatch({ type: 'TEST', payload: props.history.push }) }}
        >
            Кнопка
        </button>
        <div>
            { testData }
        </div>
    </>;
}

export default withRouter(TestContainer)