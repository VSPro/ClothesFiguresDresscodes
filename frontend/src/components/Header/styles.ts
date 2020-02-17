import { makeStyles } from "@material-ui/core/styles";

export const useStyles = makeStyles(theme => ({
    toolBarSecondary: {
      justifyContent: 'space-between',
      overflowX: 'auto',
    },
    toolBarLabel: {
      flexBasis: 200,
    },
  
    toolBarLink: {
      padding: theme.spacing(1),
      flexShrink: 0,
    },
  }));