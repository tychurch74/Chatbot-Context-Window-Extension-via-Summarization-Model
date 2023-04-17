import tensorflow as tf

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
    img_ds_from_dir,
    get_flowers_dataset,
)


# Set to True to enable model visualization and saving
plot_viz = False
save_models = False

# Check if GPU is available
gpu = len(tf.config.list_physical_devices("GPU")) > 0
print("GPU is", "available" if gpu else "NOT AVAILABLE")

# Set hyperparameters
epochs = 5
batch_size = 32
image_size = (28, 28)

# Get image dataset
train_ds, val_ds = img_ds_from_dir(get_flowers_dataset(), image_size)
class_names = train_ds.class_names
num_classes = len(class_names)
print(class_names, num_classes)
img_wd, img_ht = image_size

# Build model (input_shape, num_classes)
cnn = build_cnn((img_wd, img_ht, 1), num_classes)

if plot_viz:
    # Visualize model architecture
    viz_model(cnn, "cnn.png")
    viz_model(rnn, "rnn.png")
    viz_model(lstm, "LSTM.png")

    # Print model summary
    cnn.summary()
    rnn.summary()
    lstm.summary()

elif not plot_viz:
    print("Model visualization is disabled. Set plot_viz to True to enable it.")

# Compile model
compile_model(cnn)


def test_model(model, save_models, epochs):
    if save_models:
        # Train CNN model on mnist data
        history = train_model(model, train_ds, validation_data=val_ds, epochs=epochs)

        # Save CNN checkpoint
        save_checkpoint(model, "model.ckpt")

        # Save CNN model
        save_model(model, "model.h5")

        # Evaluate CNN model
        plot_performance(history, filename="performance.png")
        print(evaluate_model(model, val_ds))

    elif not save_models:
        print("Model saving is disabled. Set save_models to True to enable it.")
        train_model(model, train_ds, validation_data=val_ds, epochs=epochs)


test_model(model=cnn, save_models=save_models, epochs=epochs)
