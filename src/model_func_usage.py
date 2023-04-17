from models.tf_models_utils import (
    viz_model,
    build_cnn,
    build_rnn,
    build_lstm,
    compile_model,
    mnist_data,
    train_model,
    evaluate_model,
    plot_performance,
    save_model,
    save_checkpoint,
)

# Build model (input_shape, num_classes)
cnn = build_cnn((28, 28, 1), 10)
rnn = build_rnn((28, 1), 10)
lstm = build_lstm((28, 1), 10)

# Visualize model architecture
viz_model(cnn, "cnn.png")
viz_model(rnn, "rnn.png")
viz_model(lstm, "LSTM.png")

# Print model summary
cnn.summary()
rnn.summary()
lstm.summary()

# Compile model
compile_model(cnn)
compile_model(rnn)
compile_model(lstm)

# Get mnist data for CNN
x_train, y_train, x_test, y_test = mnist_data()

# Train CNN model on mnist data
history = train_model(cnn, x_train, y_train, epochs=1)

# Save CNN checkpoint
save_checkpoint(cnn, "cnn.ckpt")

# Save CNN model
save_model(cnn, "cnn.h5")

# Evaluate CNN model
plot_performance(history, filename="performance.png")
print(evaluate_model(cnn, x_test, y_test))
