import * as React from "react";
import CircularProgress, { CircularProgressProps } from "@mui/material/CircularProgress";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";

function CircularProgressWithLabel(props) {
  return (
    <div>
      <Box sx={{ position: "relative", display: "inline-flex" }}>
        <CircularProgress variant="determinate" {...props} />
        <Box
          sx={{
            top: 0,
            left: 0,
            bottom: 0,
            right: 0,
            position: "absolute",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <Typography variant="caption" component="div" color="text.secondary">
            {`${Math.round(props.value)}%`}
          </Typography>
        </Box>
      </Box>
    </div>
  );
}

function Loading() {
  const [progress, setProgress] = React.useState(10);
  const [agg, setAgg] = React.useState(false);
  const [enc, setEnc] = React.useState(10);
  React.useEffect(() => {
    const timer = setInterval(() => {
      setProgress((prevProgress) => (prevProgress >= 100 ? 0 : prevProgress + 10));
    }, 800);
    return () => {
      clearInterval(timer);
    };
  }, []);
  setInterval(() => {
    setAgg(true);
  }, 10000);
  setInterval(() => {
    setEnc(true);
  }, 10000);
  return (
    <div styel={{ margin: "20vh", position: "relative" }}>
      <CircularProgressWithLabel value={progress} />
      <p>Loading....</p>

      {agg && <p>Aggrigating data ...</p>}
      {enc && <p>Encrypting / Decrypting data with ECC ...</p>}
    </div>
  );
}

export default Loading;
