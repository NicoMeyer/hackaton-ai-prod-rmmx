class LiquidationsController < ApplicationController
  def create
    @liquidation = Liquidation.new(liquidation_params)
    @liquidation.save
    redirect_to @liquidation
  end

  private

  def liquidation_params
    params.require(:liquidation).permit(:employee_name, :base_salary)
  end
end
