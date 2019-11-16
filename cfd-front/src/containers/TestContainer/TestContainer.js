import React, { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'

function App() {

    const dispatch = useDispatch()
    const testData = useSelector( store => store.test.testItem )

    return <>
        <button
            onClick={() => { dispatch({ type: 'TEST', payload: 'some text' }) }}
        >
            Кнопка
        </button>
        <div>
            { testData }
        </div>
    </>;
  }
  
  export default App;