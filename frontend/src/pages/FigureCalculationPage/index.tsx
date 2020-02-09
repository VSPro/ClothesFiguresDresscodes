import React, { /* useState */ } from "react";
import { /* useDispatch */ useSelector } from "react-redux";
import { withRouter } from "react-router-dom";
import Button from "@material-ui/core/Button";

const FigureCalculationPageContainer = (props: any) => {
  // const dispatch = useDispatch();
  const testData = useSelector((store: any) => store.figureCalculationPage.testItem);

  // console.log('I\'m called from FigureCalculationPageContainer component', props)
  return (
    <>
      <p>Figure calculation Page</p>
      <Button
        variant="outlined"
        color="primary"
        onClick={() => {
          // dispatch({ type: "CALCULATE", payload: props.history.push });
          props.history.push('/');
        }}
      >
        На главную
      </Button>
      <div>{testData}</div>
    </>
  );
}

export default withRouter(FigureCalculationPageContainer);
