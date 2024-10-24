class CreateLiquidations < ActiveRecord::Migration[6.1]
  def change
    create_table :liquidations do |t|
      t.string :employee_name, null: false
      t.decimal :base_salary, precision: 10, scale: 2, null: false
      t.string :bonus_amount, default: 0

      t.timestamps
    end
  end
end
