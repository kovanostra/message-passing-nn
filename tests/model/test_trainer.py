from unittest import TestCase

import torch as to
from message_passing_nn.infrastructure.graph_dataset import GraphDataset

from message_passing_nn.data.data_preprocessor import DataPreprocessor
from message_passing_nn.model.trainer import Trainer
from tests.fixtures.matrices_and_vectors import BASE_GRAPH, BASE_GRAPH_NODE_FEATURES


class TestTrainer(TestCase):
    def setUp(self) -> None:
        time_steps = 1
        loss_function = "MSE"
        optimizer = "SGD"
        model = "RNN"
        device = "cpu"
        self.configuration_dictionary = {"model": model,
                                         "loss_function": loss_function,
                                         "optimizer": optimizer,
                                         "time_steps": time_steps}
        data_preprocessor = DataPreprocessor()
        self.model_trainer = Trainer(data_preprocessor, device, normalize=True)

    def test_instantiate_attributes(self):
        # Given
        number_of_nodes = BASE_GRAPH.size()[0]
        number_of_node_features = BASE_GRAPH_NODE_FEATURES.size()[1]
        data_dimensions = (BASE_GRAPH_NODE_FEATURES.size(), BASE_GRAPH.view(-1).size())

        # When
        self.model_trainer.instantiate_attributes(data_dimensions, self.configuration_dictionary)

        # Then
        self.assertTrue(self.model_trainer.model.number_of_nodes == number_of_nodes)
        self.assertTrue(
            self.model_trainer.model.number_of_node_features == number_of_node_features)
        self.assertTrue(self.model_trainer.optimizer.param_groups)

    def test_do_train(self):
        # Given
        data_dimensions = (BASE_GRAPH_NODE_FEATURES.size(), BASE_GRAPH.view(-1).size())
        self.model_trainer.instantiate_attributes(data_dimensions,
                                                  self.configuration_dictionary)
        all_neighbors = to.tensor([[1, 2, -1, -1],
                                   [0, 2, -1, -1],
                                   [0, 1, 3, -1],
                                   [2, -1, -1, -1]])
        dataset = GraphDataset("")
        dataset.enable_test_mode()
        tag = 'tag'
        dataset.dataset = [(BASE_GRAPH_NODE_FEATURES, all_neighbors, BASE_GRAPH.view(-1), tag)]
        training_data, _, _ = DataPreprocessor().train_validation_test_split(dataset, 1, 0.0, 0.0)

        # When
        training_loss = self.model_trainer.do_train(training_data=training_data, epoch=1)

        # Then
        self.assertTrue(training_loss > 0.0)

    def test_do_evaluate(self):
        # Given
        data_dimensions = (BASE_GRAPH_NODE_FEATURES.size(), BASE_GRAPH.view(-1).size())
        self.model_trainer.instantiate_attributes(data_dimensions,
                                                  self.configuration_dictionary)
        all_neighbors = to.tensor([[1, 2, -1, -1],
                                   [0, 2, -1, -1],
                                   [0, 1, 3, -1],
                                   [2, -1, -1, -1]])
        dataset = GraphDataset("")
        dataset.enable_test_mode()
        tag = 'tag'
        dataset.dataset = [(BASE_GRAPH_NODE_FEATURES, all_neighbors, BASE_GRAPH.view(-1), tag)]
        training_data, _, _ = DataPreprocessor().train_validation_test_split(dataset, 1, 0.0, 0.0)

        # When
        validation_loss = self.model_trainer.do_evaluate(evaluation_data=training_data, epoch=1)

        # Then
        self.assertTrue(validation_loss > 0.0)
