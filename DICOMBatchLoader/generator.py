"""Generates batches of DICOM image and mask data"""

from keras.preprocessing.image import ImageDataGenerator

class GeneratorFactory(object):
    """A factory for creating Python Generators

    This uses the keras keras.preprocessing.image.ImageDataGenerator class to create
    a generator and yield it for images. It is abstracted out for easy migration
    to different frameworks for generators.

    Pass a True value for `augment` if you want to fit on randomly augmented samples
    through Keras.

    How to use:
    > import generator
    > factory = generator.GeneratorFactory({zca_whitening=True}, batch_size=16, augment=True)
    > created_generator = factory.create(my_np_dicoms, my_np_masks)
    > your_keras_model.fit_generator(created_generator, steps_per_epoch=2000, epochs=50)
    """

    def __init__(self, keras_gen_args={}, batch_size=8, seed=1337, augment=False):
        self.keras_gen_args = keras_gen_args
        self.batch_size = batch_size
        self.seed = seed
        self.augment = augment


    def create(self, dicoms, masks):
        """Have the Factory create a Generator for the given dicoms and masks"""
        dicom_datagen = ImageDataGenerator(**self.keras_gen_args)
        mask_datagen = ImageDataGenerator(**self.keras_gen_args)

        # Provide the same seed and keyword arguments to the fit and flow methods
        dicom_datagen.fit(dicoms, augment=self.augment, seed=self.seed)
        mask_datagen.fit(masks, augment=self.augment, seed=self.seed)

        dicom_generator = dicom_datagen.flow(dicoms, masks, seed=self.seed,
                                             batch_size=self.batch_size, shuffle=True)
        mask_generator = mask_datagen.flow(dicoms, masks, seed=self.seed,
                                           batch_size=self.batch_size, shuffle=True)

        # Combine generators into one which yields dicom and masks
        return zip(dicom_generator, mask_generator)

# >>> import wrangler
# >>> data_dir = '/Users/ramaneekgill/Development/Practise/arterys/final_data/'
# >>> x, y = wrangler.wrangle(data_dir, data_dir + 'link.csv')
# >>> import generator