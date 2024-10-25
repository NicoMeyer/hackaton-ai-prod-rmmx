require "test_helper"

class AnimalTest < ActiveSupport::TestCase
  def setup
    @animal = Animal.new(especie: "Perro", edad: 3)
  end

  test "should be valid" do
    assert @animal.valid?
  end
end
