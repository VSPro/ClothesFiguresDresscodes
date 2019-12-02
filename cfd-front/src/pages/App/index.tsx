
import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux'
// import logo from './logo.svg';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import ToggleButton from '@material-ui/lab/ToggleButton';
import ToggleButtonGroup from '@material-ui/lab/ToggleButtonGroup';
import Box from '@material-ui/core/Box';

import { Container } from '@material-ui/core';
import './App.css';

// import TestContainer from '../TestContainer/'

function App( props: any ) {
  
  const [inputs, setInputs] = useState<any>({
    first: '',
    second: '',
    third: '',
    fourth: '',
    fifth: 'm',
    sixth: ''
  })
  const typeOfShape = useSelector( (state: any): Array<number | string> => state.app.paramsOfUser.shape)
  const size = useSelector( (state: any): {sizeOfChest: string, sizeOfHips: string} => state.app.paramsOfUser.sizeParams)

  const inputValidationFunc = (field: string) => {
    return ( e: any, newAlignment: any ) => { 
      const value = e.target.value 
      // Здесь можно добавить проверок, но всё это надо выносить в отдельный компонент
      if(isNaN(+value)) {
        setInputs(
          (state: any) => {
            return {...state, [field]: newAlignment}
          }
        )
      }
      setInputs(
        (state: any) => {
          return {...state, [field]: value}
        }
      )
    }
  }

  const dispatch = useDispatch()

  return (
    // <div className="App">
    <section className="App-header">
    {/* <section> */}
      <ToggleButtonGroup
        value={inputs.fifth}
        exclusive
        onChange={inputValidationFunc('fifth')}
        aria-label="text alignment"
      >
        <ToggleButton value="m" aria-label="left aligned">
          М
        </ToggleButton>
        <ToggleButton value="f" aria-label="centered">
          Ж
        </ToggleButton>
      </ToggleButtonGroup>
      <TextField
        id="chest-girth"
        label="Ширина плеч"
        variant="outlined"
        // fullWidth
        margin="normal"
        type='number'
        value={ inputs.first }
        onChange={ inputValidationFunc('first') as any}
      />
      <TextField
        id="chest-girth"
        label="Обхват груди"
        variant="outlined"
        // fullWidth
        margin="normal"
        type='number'
        value={ inputs.sixth }
        onChange={ inputValidationFunc('sixth') as any}
      />
      <TextField
        id="waist-circumference"
        label="Обхват талии"
        variant="outlined"
        margin="normal"
        type='number'
        value={ inputs.second }
        onChange={ inputValidationFunc('second') as any}
      />
      <TextField
        id="hip-girth"
        label="Обхват бёдер"
        variant="outlined"
        margin="normal"
        type='number'
        value={ inputs.third }
        onChange={ inputValidationFunc('third') as any }
      />
      <TextField
        id="height"
        label="Рост"
        variant="outlined"
        margin="normal"
        type='number'
        value={ inputs.fourth }
        onChange={ inputValidationFunc('fourth') as any }
      />
      <Button
        variant="contained"
        color="secondary"
        disabled={ !(inputs.first && inputs.second && inputs.third && inputs.fourth && inputs.fifth && inputs.sixth) } 
        onClick={ () => { 
          dispatch(
            {
              type: 'SHAPE_METRICS', 
              payload: {
                shoulders: inputs.first,
                chest: inputs.sixth,
                waist: inputs.second,
                hips: inputs.third,
                height: inputs.fourth,
                sex: inputs.fifth
              } 
            }
          ) 
        }}
      >
        Определить тип фигуры  
      </Button>

      <article>
        <div>Ваш тип фигуры:</div>
        { typeOfShape }
        <div>Ваш размер</div>
        <p> по плечам: { size.sizeOfChest } </p>
        <p> по бёдрам: { size.sizeOfHips } </p>
      </article>

      {/* <TestContainer /> */}
    </section>
  );
}

export default App;
