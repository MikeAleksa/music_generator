from pathlib import Path
from unittest import TestCase

import mido

from music_generator.serializers.discrete_time_serializer import DiscreteTimeMidiSerializer


class TestDiscreteTimeMidiSerializer(TestCase):
    def setUp(self) -> None:
        self.serializer = DiscreteTimeMidiSerializer(wait_classes=128)

    def test_serialize(self):
        """
        Check if a simple midi file can be serialized to a sequence.
        """
        test_midi_file = 'test_midi/test_midi_002.mid'
        sequence = self.serializer.serialize(test_midi_file)
        # midi file is the same as the one that should be created in test_sequence_to_midi
        expected_sequence = []
        for i in range(128):
            expected_sequence.append(i + 256)
            expected_sequence.append(i)
            expected_sequence.append(i + 256)
            expected_sequence.append(i + 128)
        self.assertListEqual(expected_sequence, sequence)

    def test_deserialize(self):
        """
        Check if a simple sequence can be correctly deserialized to MIDI.
        """
        test_sequence = []
        for i in range(128):
            # append increasing wait, note on, wait note off
            test_sequence.append(i + 256)
            test_sequence.append(i)
            test_sequence.append(i + 256)
            test_sequence.append(i + 128)

        # save the resulting sequence
        self.serializer.deserialize(test_sequence, './test_midi/', 'test_midi_001.mid')

        # load resulting sequence in mido
        midi = mido.MidiFile('test_midi/test_midi_001.mid')

        # check sequence
        i = 0
        messages = [msg for msg in midi]
        for m1, m2 in zip(messages[::2], messages[1::2]):
            self.assertTrue('note_on' == m1.type)
            self.assertTrue(i == m1.note)
            self.assertAlmostEqual((i + 1) / self.serializer.samples, round(m1.time, 10))
            self.assertTrue('note_off' == m2.type)
            self.assertTrue(i == m2.note)
            self.assertAlmostEqual((i + 1) / self.serializer.samples, round(m2.time, 10))
            i += 1

    def test_bach_chorale_serialize(self):
        """
        Check if all bach chorale MIDI files can be successfully serialized to sequences and back to MIDI.
        """
        paths = Path('./test_midi/bach_chorales_midi').glob('*.mid')
        for path in paths:
            sequence = self.serializer.serialize(path)
            self.serializer.deserialize(sequence, './test_midi/', 'converted.mid')
            converted_sequence = self.serializer.serialize('./test_midi/converted.mid')
            self.assertListEqual(sequence, converted_sequence)
