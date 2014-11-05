--
-- Author: @author@
-- Create Date: @date@
--
entity @tb_name@ is
end @tb_name@

architecture <TYPE> of @tb_name@ is
--
	component @module_name@
	port(
	);
	end component;
--
begin
	uut: @module_name@ port map(
	);
--
	tb: process
	begin
		wait for 100 ns;
		--
		-- code goes here
		--
		wait;
	end process;
end <TYPE>;
