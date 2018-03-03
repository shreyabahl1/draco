class PropObjects:
  """
  Functions to retrieve objects for fields that require object values
  """
  
  @staticmethod
  def get_bin(max_bins):
    """
    Returns a bin object with given max_bins
    """
    return { 'maxbins': max_bins }

  @staticmethod
  def unpack_bin(bin_obj):
    return bin_obj['maxbins']

  @staticmethod
  def get_scale(scale_enum):
    """
    Returns a scale object for the given type.

    type -- `zero` or `log`
    """
    if (scale_enum == 'zero'):
      return { 'type': 'linear', 'zero': True }
    elif (scale_enum == 'log'):
      return { 'type': 'log' }
    else:
      raise ValueError('scale should be zero or log')

  @staticmethod
  def unpack_scale(scale_obj):
    scale_type = scale_obj['type']

    if (scale_type == 'linear' and 'zero' in scale_obj and scale_obj['zero']):
      return 'zero'
    elif (scale_type == 'log'):
      return 'log'