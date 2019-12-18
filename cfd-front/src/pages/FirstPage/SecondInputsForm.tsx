import React, { useState } from "react";
import { useDispatch } from "react-redux";
import { withRouter } from "react-router-dom";
import { SwatchesPicker } from "react-color";

import Button from "@material-ui/core/Button";
import TextField from "@material-ui/core/TextField";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";

import InputLabel from "@material-ui/core/InputLabel";
import MenuItem from "@material-ui/core/MenuItem";
import FormHelperText from "@material-ui/core/FormHelperText";
import FormControl from "@material-ui/core/FormControl";
import Select from "@material-ui/core/Select";
import PhotoViewer from "./PhotoViewer";

const useStyles = makeStyles(theme => ({
  form: {
    width: "100%", // Fix IE 11 issue.
    marginTop: theme.spacing(3)
  },
  submit: {
    margin: theme.spacing(3, 0, 2)
  },
  colorPickerButton: {
    margin: theme.spacing(3, 0, 2),
    height: 50,
    backgroundColor: "red"
  },
  titleForToggle: {
    marginTop: theme.spacing(1)
  },
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120
  },
  cardMedia: {
    paddingTop: "56.25%" // 16:9
  },
  card: {
    height: "100%",
    display: "flex",
    flexDirection: "column"
  }
}));

const SecondInputForm = (props: any) => {
  const isDisable = props.isDisable;
  const classes = useStyles();

  const [inputs] = useState<any>({
    fourth: ""
  });
  const [isHairColorPickerShow, setShowingOfHairColorPicker] = useState<any>(
    false
  );
  const [isSkinColorPickerShow, setShowingOfSkinColorPicker] = useState<any>(
    false
  );
  const [colorOfHair, setColorOfHair] = useState<any>("#ff5722");
  const [colorOfSkin, setColorOfSkin] = useState<any>("#ffecb3");

  const [posture, setPosture] = useState<any>("");
  const [legs, setLegs] = useState<any>("");
  const [age, setAge] = useState<any>("");

  // const typeOfShape = useSelector( (state: any): Array<number | string> => state.app.paramsOfUser.shape)
  // const size = useSelector( (state: any): {sizeOfChest: string, sizeOfHips: string} => state.app.paramsOfUser.sizeParams)

  const dispatch = useDispatch();

  return (
    <form className={classes.form} noValidate>
      <Grid container spacing={2}>
        <Grid item xs={12} sm={6}>
          <Button
            fullWidth
            variant="contained"
            style={{
              backgroundColor: colorOfHair
            }}
            className={classes.colorPickerButton}
            onClick={() => {
              setShowingOfHairColorPicker(!isHairColorPickerShow);
            }}
          >
            цвет волос*
          </Button>
          {isHairColorPickerShow ? (
            <div
              style={{
                position: "absolute",
                zIndex: 1
              }}
            >
              <SwatchesPicker
                onChange={(e: any) => {
                  setColorOfHair(e.hex);
                }}
              />
            </div>
          ) : null}
        </Grid>
        <Grid item xs={12} sm={6}>
          <Button
            fullWidth
            variant="contained"
            style={{
              backgroundColor: colorOfSkin
            }}
            className={classes.colorPickerButton}
            onClick={() => {
              setShowingOfSkinColorPicker(!isSkinColorPickerShow);
            }}
          >
            цвет кожи
          </Button>
          {isSkinColorPickerShow ? (
            <div
              style={{
                position: "absolute",
                zIndex: 1
              }}
            >
              <SwatchesPicker
                onChange={(e: any) => {
                  setColorOfSkin(e.hex);
                }}
              />
            </div>
          ) : null}
        </Grid>
        <Grid item xs={12} sm={6}>
          <FormControl className={classes.formControl}>
            <InputLabel id="demo-simple-select-helper-label">Ноги</InputLabel>
            <Select
              labelId="demo-simple-select-helper-label"
              id="demo-simple-select-helper"
              value={legs}
              onChange={e => {
                setLegs(e.target.value);
              }}
            >
              <MenuItem value="">
                <em>Не выбранно</em>
              </MenuItem>
              <MenuItem value={-1}>Выгнутые</MenuItem>
              <MenuItem value={0}>Нормальные</MenuItem>
              <MenuItem value={1}>Вогнутые</MenuItem>
            </Select>
            <FormHelperText>См. статью "Об осанке и ногах"**</FormHelperText>
          </FormControl>
        </Grid>
        <Grid item xs={12} sm={6}>
          <FormControl className={classes.formControl}>
            <InputLabel id="demo-simple-select-helper-label">Осанка</InputLabel>
            <Select
              labelId="demo-simple-select-helper-label"
              id="demo-simple-select-helper"
              value={posture}
              onChange={e => {
                setPosture(e.target.value);
              }}
            >
              <MenuItem value="">
                <em>Не выбранно</em>
              </MenuItem>
              <MenuItem value={-1}>Лордоз</MenuItem>
              <MenuItem value={0}>Плоская спина</MenuItem>
              <MenuItem value={1}>Сутулость</MenuItem>
            </Select>
            <FormHelperText>См. статью "Об осанке и ногах"**</FormHelperText>
          </FormControl>
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            id="waist-circumference"
            label="Возраст"
            margin="normal"
            type="number"
            value={age}
            onChange={e => {
              setAge(e.target.value);
            }}
          />
        </Grid>
        <Grid item xs={12} sm={12}>
          <Typography
            variant="subtitle2"
            noWrap
            className={classes.titleForToggle}
          >
            *Если волос нет, задайте цвет такой же, как цвет кожи
          </Typography>
          <Typography
            variant="subtitle2"
            noWrap
            className={classes.titleForToggle}
          >
            **Статью можно найти в меню справа
          </Typography>
        </Grid>
        <Button
          fullWidth
          variant="outlined"
          color="secondary"
          className={classes.submit}
          disabled={
            !(
              colorOfSkin &&
              colorOfHair &&
              legs !== "" &&
              posture !== "" &&
              age !== "" &&
              !isDisable
            )
          }
          onClick={() => {
            dispatch({
              type: "APPEARANCE_FEATURES",
              payload: {
                colorOfSkin: colorOfSkin,
                colorOfHair: colorOfHair,
                curvatureOfLegs: legs,
                curvatureOfBack: posture,
                age: inputs.fourth
              }
            });
          }}
        >
          Подобрать снимки схожих с Вами людей
        </Button>
        <PhotoViewer />
        <Button
          fullWidth
          variant="contained"
          color="secondary"
          className={classes.submit}
          disabled={
            !(
              colorOfSkin &&
              colorOfHair &&
              legs !== "" &&
              posture !== "" &&
              age !== "" &&
              !isDisable
            )
          }
          onClick={e => {
            props.history.push("/filters");
          }}
        >
          Перейти к подбору одежды
        </Button>
      </Grid>
    </form>
  );
};

export default withRouter(SecondInputForm);
