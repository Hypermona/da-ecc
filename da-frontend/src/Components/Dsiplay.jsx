export default function Display({ sink, base, enc, dec, images }) {
  return (
    <div>
      <p>
        <strong>Encrypted Data At Sink Node: </strong> {sink}
      </p>

      <p>
        <strong>Decrypted Data At Base Node: </strong>
        {base}
      </p>

      <p>
        <strong>Encryptio Time:</strong> {enc} S
      </p>

      <p>
        <strong>Decryption Time:</strong> {dec} S
      </p>
      {images.map((image, i) => (
        <img src={`data:image/png;base64,${image}`} alt="" key={i} />
      ))}
    </div>
  );
}
