class Liquidation < ApplicationRecord
  validates :employee_name, presence: true
  validates :base_salary, presence: true, numericality: { greater_than: 0 }

  # Error: Suma incorrecta entre decimal y string
  def total_salary
    base_salary + bonus_amount
  end
end
