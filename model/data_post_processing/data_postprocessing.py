class PostProcessor:
    def save_predictions_to_csv(self, predictions, output_path):
        predictions.to_csv(output_path, index=False)
